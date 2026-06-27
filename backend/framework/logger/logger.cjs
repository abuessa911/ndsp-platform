'use strict';

function createLogger(meta = {}) {
  const base = {
    service_id: meta.serviceId || meta.service_id || 'UNKNOWN',
    service_name: meta.serviceName || meta.service_name || 'UNKNOWN',
    component: meta.component || 'NDSP'
  };

  function write(level, message, extra = {}) {
    const line = { timestamp: new Date().toISOString(), level, message, ...base, ...extra };
    const out = JSON.stringify(line);
    if (level === 'error') console.error(out);
    else console.log(out);
  }

  return {
    info: (message, extra) => write('info', message, extra),
    warn: (message, extra) => write('warn', message, extra),
    error: (message, extra) => write('error', message, extra),
    child: (extra = {}) => createLogger({ ...base, ...extra })
  };
}

module.exports = { createLogger };
