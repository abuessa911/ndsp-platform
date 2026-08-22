'use strict';

const http = require('http');
const https = require('https');
const { URL } = require('url');

const PORT = Number(process.env.PORT || 8097);
const CACHE_TTL_MS = Number(process.env.CACHE_TTL_MS || 600000);
const REFRESH_INTERVAL_MS = Number(process.env.REFRESH_INTERVAL_MS || 600000);
const FETCH_TIMEOUT_MS = Number(process.env.FETCH_TIMEOUT_MS || 7000);
const MAX_ITEMS = Number(process.env.MAX_ITEMS || 20);

function splitEnv(value) {
  return String(value || '')
    .split(',')
    .map(v => v.trim())
    .filter(Boolean);
}

const INVESTING_RSS_URLS = splitEnv(process.env.INVESTING_RSS_URLS || [
  'https://www.investing.com/rss/news.rss',
  'https://www.investing.com/rss/news_25.rss',
  'https://www.investing.com/rss/news_1.rss'
].join(','));

const BLOOMBERG_RSS_URLS = splitEnv(process.env.BLOOMBERG_RSS_URLS || [
  'https://news.google.com/rss/search?q=site%3Abloomberg.com%20when%3A24h&hl=en-US&gl=US&ceid=US%3Aen'
].join(','));

const FEEDS = [
  ...BLOOMBERG_RSS_URLS.map(url => ({ source: 'Bloomberg', url })),
  ...INVESTING_RSS_URLS.map(url => ({ source: 'Investing.com', url }))
];

let cache = {
  ok: false,
  generatedAt: null,
  stale: true,
  items: [],
  errors: [],
  sourceCount: FEEDS.length,
  note: 'Headlines and source links only. Full articles remain on original publisher sites.'
};

let lastFetchAt = 0;
let refreshing = false;

function decodeXml(value) {
  return String(value || '')
    .replace(/<!\[CDATA\[(.*?)\]\]>/gs, '$1')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#039;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/\s+/g, ' ')
    .trim();
}

function pick(block, tag) {
  const re = new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)<\\/${tag}>`, 'i');
  const m = block.match(re);
  return m ? decodeXml(m[1]) : '';
}

function cleanTitle(title, source) {
  let t = decodeXml(title);
  if (source === 'Bloomberg') {
    t = t.replace(/\s+-\s+Bloomberg(\.com)?$/i, '').trim();
  }
  if (source === 'Investing.com') {
    t = t.replace(/\s+-\s+Investing\.com$/i, '').trim();
  }
  return t;
}

function parseRss(xml, source) {
  const out = [];

  const itemRegex = /<item\b[^>]*>([\s\S]*?)<\/item>/gi;
  let m;

  while ((m = itemRegex.exec(xml)) !== null) {
    const block = m[1];
    const title = cleanTitle(pick(block, 'title'), source);
    const link = decodeXml(pick(block, 'link') || pick(block, 'guid'));
    const pubDateText = pick(block, 'pubDate') || pick(block, 'updated') || pick(block, 'published');
    const date = pubDateText ? new Date(pubDateText) : null;

    if (!title || title.length < 8) continue;

    out.push({
      source,
      title,
      url: link,
      publishedAt: date && !Number.isNaN(date.getTime()) ? date.toISOString() : null
    });
  }

  const entryRegex = /<entry\b[^>]*>([\s\S]*?)<\/entry>/gi;

  while ((m = entryRegex.exec(xml)) !== null) {
    const block = m[1];
    const title = cleanTitle(pick(block, 'title'), source);
    const linkMatch = block.match(/<link\b[^>]*href=["']([^"']+)["'][^>]*>/i);
    const link = decodeXml(linkMatch ? linkMatch[1] : pick(block, 'link'));
    const dateText = pick(block, 'updated') || pick(block, 'published');
    const date = dateText ? new Date(dateText) : null;

    if (!title || title.length < 8) continue;

    out.push({
      source,
      title,
      url: link,
      publishedAt: date && !Number.isNaN(date.getTime()) ? date.toISOString() : null
    });
  }

  return out;
}

function fetchUrl(url, redirects = 0) {
  return new Promise((resolve, reject) => {
    let parsed;

    try {
      parsed = new URL(url);
    } catch (err) {
      reject(err);
      return;
    }

    const lib = parsed.protocol === 'http:' ? http : https;

    const req = lib.get({
      protocol: parsed.protocol,
      hostname: parsed.hostname,
      port: parsed.port || undefined,
      path: parsed.pathname + parsed.search,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; NDSP-NewsTicker/2.0; +https://ndsp.app)',
        'Accept': 'application/rss+xml, application/xml, text/xml, */*',
        'Cache-Control': 'no-cache'
      },
      timeout: FETCH_TIMEOUT_MS
    }, res => {
      const status = Number(res.statusCode || 0);

      if ([301, 302, 303, 307, 308].includes(status) && res.headers.location && redirects < 3) {
        res.resume();
        const nextUrl = new URL(res.headers.location, url).toString();
        fetchUrl(nextUrl, redirects + 1).then(resolve).catch(reject);
        return;
      }

      let data = '';
      res.setEncoding('utf8');

      res.on('data', chunk => {
        data += chunk;
        if (data.length > 2_000_000) {
          req.destroy(new Error('RESPONSE_TOO_LARGE'));
        }
      });

      res.on('end', () => {
        if (status < 200 || status >= 400) {
          reject(new Error(`HTTP_${status}`));
          return;
        }

        resolve(data);
      });
    });

    req.on('timeout', () => req.destroy(new Error('TIMEOUT')));
    req.on('error', reject);
  });
}

async function fetchFeed(feed) {
  const xml = await fetchUrl(feed.url);
  return parseRss(xml, feed.source);
}

async function refreshNews(reason = 'scheduled') {
  if (refreshing) return cache;

  refreshing = true;
  const started = Date.now();

  try {
    const results = await Promise.allSettled(FEEDS.map(fetchFeed));
    const errors = [];
    const items = [];

    results.forEach((result, index) => {
      const feed = FEEDS[index];

      if (result.status === 'fulfilled') {
        items.push(...result.value);
      } else {
        errors.push({
          source: feed.source,
          url: feed.url,
          error: result.reason && result.reason.message ? result.reason.message : String(result.reason)
        });
      }
    });

    const seen = new Set();
    const deduped = [];

    for (const item of items) {
      const key = `${item.source}::${item.title}`.toLowerCase();
      if (seen.has(key)) continue;
      seen.add(key);
      deduped.push(item);
    }

    deduped.sort((a, b) => {
      const ad = a.publishedAt ? Date.parse(a.publishedAt) : 0;
      const bd = b.publishedAt ? Date.parse(b.publishedAt) : 0;
      return bd - ad;
    });

    if (deduped.length > 0) {
      cache = {
        ok: true,
        generatedAt: new Date().toISOString(),
        stale: false,
        items: deduped.slice(0, MAX_ITEMS),
        errors,
        sourceCount: FEEDS.length,
        refreshMs: Date.now() - started,
        refreshReason: reason,
        note: 'Headlines and source links only. Full articles remain on original publisher sites.'
      };

      lastFetchAt = Date.now();
    } else {
      cache = {
        ...cache,
        ok: cache.items.length > 0,
        generatedAt: cache.generatedAt || new Date().toISOString(),
        stale: true,
        errors,
        sourceCount: FEEDS.length,
        refreshMs: Date.now() - started,
        refreshReason: reason
      };
    }
  } catch (err) {
    cache = {
      ...cache,
      ok: cache.items.length > 0,
      stale: true,
      errors: [{
        source: 'system',
        error: err && err.message ? err.message : String(err)
      }],
      refreshMs: Date.now() - started,
      refreshReason: reason
    };
  } finally {
    refreshing = false;
  }

  return cache;
}

function maybeRefresh(reason) {
  const now = Date.now();
  const cacheAge = now - lastFetchAt;

  if (!refreshing && (!cache.generatedAt || cacheAge > CACHE_TTL_MS)) {
    refreshNews(reason).catch(err => {
      console.error('[NDSP_NEWS_TICKER_REFRESH_ERROR]', err && err.message ? err.message : err);
    });
  }
}

function sendJson(res, status, payload) {
  const body = JSON.stringify(payload);

  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store, max-age=0',
    'Access-Control-Allow-Origin': '*',
    'X-NDSP-News-Ticker': 'fast-v2'
  });

  res.end(body);
}

const server = http.createServer((req, res) => {
  const path = String(req.url || '').split('?')[0];

  if (path === '/health' || path === '/api/news-ticker/health') {
    sendJson(res, 200, {
      ok: true,
      service: 'ndsp-news-ticker',
      mode: 'fast-cache-v2',
      port: PORT,
      generatedAt: cache.generatedAt,
      stale: cache.stale,
      refreshing,
      items: cache.items.length,
      sources: FEEDS.map(f => f.source)
    });
    return;
  }

  if (path === '/api/news-ticker') {
    maybeRefresh('request');

    sendJson(res, 200, {
      ...cache,
      stale: cache.stale || (Date.now() - lastFetchAt > CACHE_TTL_MS),
      refreshing
    });
    return;
  }

  sendJson(res, 404, { ok: false, error: 'NOT_FOUND' });
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`[NDSP_NEWS_TICKER_FAST_V2] listening on 127.0.0.1:${PORT}`);
  refreshNews('startup').catch(err => console.error('[NDSP_NEWS_TICKER_STARTUP_ERROR]', err));
  setInterval(() => maybeRefresh('interval'), REFRESH_INTERVAL_MS);
});
