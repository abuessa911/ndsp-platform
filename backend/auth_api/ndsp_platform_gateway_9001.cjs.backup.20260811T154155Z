'use strict';

const http = require('http');
const { URL } = require('url');

const PORT = Number(process.env.NDSP_PLATFORM_GATEWAY_PORT || 9001);
const HOST = process.env.NDSP_PLATFORM_GATEWAY_HOST || '127.0.0.1';

const ROUTES = [
  { prefix: '/api/admin-ui/', target: 'http://127.0.0.1:9023' }, // NDSP_ADMIN_UI_PROXY_ROUTE_SAFE_20260604
  { prefix: '/api/auth/', target: 'http://127.0.0.1:9020' },
  { prefix: '/api/user-dashboard/', target: 'http://127.0.0.1:9021' },
  { prefix: '/api/trial/', target: 'http://127.0.0.1:9019' },
  { prefix: '/api/admin-actions/', target: 'http://127.0.0.1:9017' },
  { prefix: '/api/admin/', target: 'http://127.0.0.1:9017' },
  { prefix: '/api/', target: 'http://127.0.0.1:9002' }
];

function sendJson(res, code, body) {
  const payload = JSON.stringify(body);
  res.writeHead(code, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(payload),
    'Cache-Control': 'no-store',
    'X-NDSP-Gateway': 'platform-9001'
  });
  res.end(payload);
}

function matchRoute(pathname) {
  if (pathname === '/health' || pathname === '/api/health') return { health: true };

  for (const route of ROUTES) {
    if (pathname === route.prefix || pathname.startsWith(route.prefix)) return route;
  }

  return null;
}

function proxyRequest(req, res, route) {
  const target = new URL(route.target);
  const path = req.url || '/';

  const options = {
    protocol: target.protocol,
    hostname: target.hostname,
    port: target.port,
    method: req.method,
    path,
    headers: {
      ...req.headers,
      host: target.host,
      'x-ndsp-platform-gateway': '9001',
      'x-forwarded-host': req.headers.host || '',
      'x-forwarded-proto': req.headers['x-forwarded-proto'] || 'https'
    },
    timeout: 30000
  };

  const upstream = http.request(options, upstreamRes => {
    const headers = { ...upstreamRes.headers };
    headers['x-ndsp-gateway'] = 'platform-9001';
    delete headers['content-length'];
    res.writeHead(upstreamRes.statusCode || 502, headers);
    upstreamRes.pipe(res);
  });

  upstream.on('timeout', () => {
    upstream.destroy(new Error('UPSTREAM_TIMEOUT'));
  });

  upstream.on('error', err => {
    sendJson(res, 502, {
      ok: false,
      error: 'UPSTREAM_GATEWAY_ERROR',
      service: 'ndsp-platform-gateway',
      target: route.target,
      detail: String(err && err.message ? err.message : err)
    });
  });

  req.pipe(upstream);
}

const server = http.createServer((req, res) => {
  try {
    const parsed = new URL(req.url || '/', `http://${req.headers.host || 'localhost'}`);
    const route = matchRoute(parsed.pathname);

      // NDSP_CORE_ROUTE_REWRITE_20260604
      // Keep the gateway raw-http architecture. Rewrite only verified public aliases.
      const originalPathname = parsed.pathname;
      let rewrittenUrl = null;

      if (originalPathname === '/api/trial/status') rewrittenUrl = '/api/trial/status';
      if (originalPathname === '/api/trial/info') rewrittenUrl = '/api/trial/status';

      if (originalPathname === '/ops/ws-status') rewrittenUrl = '/ops/ws-status';
      if (originalPathname === '/ops/alerts-status') rewrittenUrl = '/ops/alerts-status';
      if (originalPathname === '/api/ops/ws-status') rewrittenUrl = '/ops/ws-status';
      if (originalPathname === '/api/ops/alerts-status') rewrittenUrl = '/ops/alerts-status';
      if (originalPathname === '/api/alerts/status') rewrittenUrl = '/ops/alerts-status';

      if (rewrittenUrl) {
        const rewrittenReq = Object.create(req);
        rewrittenReq.url = rewrittenUrl + (parsed.search || '');
        return proxyRequest(rewrittenReq, res, { prefix: originalPathname, target: 'http://127.0.0.1:9002' });
      }
      // NDSP_CORE_ROUTE_REWRITE_END_20260604


    if (route && route.health) {
      return sendJson(res, 200, {
        ok: true,
        service: 'ndsp-platform-gateway',
        platform_backend_port: 9001,
        bot_backend_port: 9002,
        public_api_namespace: '/api',
        legacy_services_behind_gateway: [9017, 9019, 9020, 9021]
      });
    }

    if (!route || !route.target) {
      return sendJson(res, 404, {
        ok: false,
        error: 'NOT_FOUND',
        service: 'ndsp-platform-gateway',
        path: parsed.pathname
      });
    }

    return proxyRequest(req, res, route);
  } catch (err) {
    return sendJson(res, 500, {
      ok: false,
      error: 'GATEWAY_EXCEPTION',
      detail: String(err && err.message ? err.message : err)
    });
  }
});

server.listen(PORT, HOST, () => {
  console.log(`NDSP platform gateway listening on http://${HOST}:${PORT}`);
});
