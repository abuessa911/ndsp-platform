/**
 * Security Headers Middleware
 * يسمح بفتح الموقع مع Enhanced Tracking Protection
 */

const securityHeaders = (req, res, next) => {
  // السماح بـ Tracking
  res.setHeader('Permissions-Policy', 'interest-cohort=()');
  
  // تجاوز COEP لـ embedded content
  res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');
  res.setHeader('Cross-Origin-Opener-Policy', 'same-origin-allow-popups');
  
  // السماح بـ Referer
  res.setHeader('Referrer-Policy', 'no-referrer-when-downgrade');
  
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  // Security headers
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  
  // السماح بـ Third-party cookies
  res.setHeader('Set-Cookie', 'SameSite=None; Secure');
  
  next();
};

module.exports = securityHeaders;
