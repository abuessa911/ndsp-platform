import Redis from 'ioredis';

// إعداد الاتصال بخادم Redis
export const redis = new Redis({
  host: process.env.REDIS_HOST || '127.0.0.1',
  port: Number(process.env.REDIS_PORT) || 6379,
  password: process.env.REDIS_PASSWORD || undefined,
  retryStrategy: (times) => {
    // محاولة إعادة الاتصال التلقائية
    return Math.min(times * 50, 2000);
  }
});

/**
 * القنوات الرسمية لمنظومة NDSP V4.1
 * كل طبقة ستنتج أو تستهلك من هذه القنوات لتطبيق العزل المعماري.
 */
export const NDSP_STREAMS = {
  PRICE: 'ndsp.price.stream',         // نبض السعر اللحظي
  TIMING: 'ndsp.timing.stream',       // مخرجات سلطة الوقت
  TDL: 'ndsp.tdl.stream',             // قرارات الاتجاه (Direction Authority)
  QUALITY: 'ndsp.quality.stream',     // تقييم الجودة (Quality Effect)
  RISK: 'ndsp.risk.stream',           // محرك الامتثال والفلترة العكسية
  DECISION: 'ndsp.decision.stream',   // المخرجات النهائية
  AUDIT: 'ndsp.audit.stream'          // سجل الحوكمة والعمليات
} as const;

console.log("🟢 NDSP Eventbus (Redis Streams) is initializing...");
