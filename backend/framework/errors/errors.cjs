'use strict';

class NDSPError extends Error {
  constructor(code, message, status = 500, details = {}) {
    super(message);
    this.name = 'NDSPError';
    this.code = code || 'NDSP-0000';
    this.status = status;
    this.details = details;
  }
}

function errorResponse(err, meta = {}) {
  return {
    ok: false,
    service: meta.serviceId || 'UNKNOWN',
    version: meta.version || '0.0.0',
    timestamp: new Date().toISOString(),
    error: {
      code: err.code || 'NDSP-5000',
      message: err.message || 'Internal Server Error',
      details: err.details || {}
    }
  };
}

function errorMiddleware(meta = {}, logger = console) {
  return function ndspErrorMiddleware(err, _req, res, _next) {
    const status = err.status || 500;
    if (logger && logger.error) {
      logger.error('request_error', { code: err.code || 'NDSP-5000', status, error_message: err.message });
    }
    res.status(status).json(errorResponse(err, meta));
  };
}

module.exports = { NDSPError, errorResponse, errorMiddleware };
