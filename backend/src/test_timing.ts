import { TimingPublisher } from './eventbus/publishers/TimingPublisher';
import { TimingContract } from './contracts/TimingContract';
import { redis } from './eventbus/redisClient';

async function runTest() {
  console.log("🚀 بدء اختبار ضخ البيانات في NDSP Eventbus...");

  // إنشاء كائن يطابق عقد التوقيت الصارم
  // ⚠️ جرب لاحقاً إضافة حقل 'direction' هنا، وسترى كيف يرفض TypeScript تشغيل الكود!
  const timingData: TimingContract = {
    controller: 'L&M',
    direction_source: 'tdl.weekly.lm_direction',
    day_group: 'Monday',
    decision_authority: 'Timing Authority Layer'
  };

  try {
    const id = await TimingPublisher.publish(timingData);
    console.log(`✅ نجاح: تم ضخ حدث التوقيت ومطابقة العقد بنسبة 100%. Event ID: ${id}`);
  } catch (error) {
    console.error("❌ فشل الاختبار:", error);
  } finally {
    // إغلاق الاتصال بقاعدة البيانات لإنهاء السكريبت
    redis.quit();
  }
}

runTest();
