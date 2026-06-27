'use strict';

function attachGracefulShutdown(server, logger) {
  let closing = false;

  function shutdown(signal) {
    if (closing) return;
    closing = true;
    if (logger && logger.info) logger.info('shutdown_started', { signal });
    server.close(() => {
      if (logger && logger.info) logger.info('shutdown_complete', { signal });
      process.exit(0);
    });
    setTimeout(() => {
      if (logger && logger.error) logger.error('shutdown_forced', { signal });
      process.exit(1);
    }, 8000).unref();
  }

  process.once('SIGTERM', () => shutdown('SIGTERM'));
  process.once('SIGINT', () => shutdown('SIGINT'));
}

module.exports = { attachGracefulShutdown };
