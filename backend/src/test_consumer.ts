import { TimingConsumer } from './eventbus/consumers/TimingConsumer';

console.log("🚀 تشغيل مستهلك أحداث التوقيت في وضع الانتظار...");

TimingConsumer.listen((data, eventId) => {
  console.log(`\n📥 [استلام حدث جديد!]`);
  console.log(`- 🔑 معرف الحدث (ID): ${eventId}`);
  console.log(`- ⏱️ المسيطر الزمني: ${data.controller}`);
  console.log(`- 🧭 مصدر الاتجاه: ${data.direction_source}`);
  console.log(`✅ جاهز لتمرير هذه البيانات للطبقة التالية باستقلالية تامة.\n`);
});
