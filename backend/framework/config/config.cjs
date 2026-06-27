'use strict';

const fs = require('fs');
const path = require('path');

function parseScalar(v) {
  const s = String(v || '').trim();
  if (s === 'true') return true;
  if (s === 'false') return false;
  if (s === 'null') return null;
  if (/^-?\d+(\.\d+)?$/.test(s)) return Number(s);
  return s.replace(/^["']|["']$/g, '');
}

function parseSimpleYaml(txt) {
  const out = {};
  const lines = String(txt || '').split(/\r?\n/);
  for (const raw of lines) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const idx = line.indexOf(':');
    if (idx === -1) continue;
    const key = line.slice(0, idx).trim();
    const val = line.slice(idx + 1).trim();
    out[key] = parseScalar(val);
  }
  return out;
}

function loadManifest(serviceRoot) {
  const file = path.join(serviceRoot || process.cwd(), 'service.yaml');
  if (!fs.existsSync(file)) return {};
  return parseSimpleYaml(fs.readFileSync(file, 'utf8'));
}

function loadConfig(options = {}) {
  const env = process.env;
  const serviceRoot = options.serviceRoot || process.cwd();
  const manifest = loadManifest(serviceRoot);
  return {
    env: env.NODE_ENV || 'production',
    host: env.NDSP_HOST || env.HOST || manifest.host || '127.0.0.1',
    port: Number(env.NDSP_PORT || env.PORT || manifest.port || options.port || 0),
    manifest,
    serviceRoot
  };
}

module.exports = { loadConfig, loadManifest, parseSimpleYaml };
