import { redis, NDSP_STREAMS } from '../redisClient';
import { TimingContract } from '../../contracts/TimingContract';

export class TimingConsumer {
  /**
   * الاستماع المستمر لمجرى أحداث التوقيت
   * @param callback الدالة التي ستنفذ عند وصول حدث جديد
   */
  static async listen(callback: (data: TimingContract, eventId: string) => void) {
    console.log(`🎧 [Layer 6 / TDL Consumer] Listening for new events on ${NDSP_STREAMS.TIMING}...`);

    let lastId = '$'; // '$' تعني الاستماع للأحداث الجديدة فقط من لحظة التشغيل

    while (true) {
      try {
        // استخدام XREAD BLOCK للانتظار حتى وصول رسالة جديدة (بدون استهلاك موارد المعالج)
        const streamResult = await redis.xread(
          'BLOCK', 0, 
          'STREAMS', NDSP_STREAMS.TIMING, lastId
        );

        if (streamResult) {
          const [stream] = streamResult;
          const messages = stream[1];

          for (const message of messages) {
            lastId = message[0]; // تحديث الـ ID لتجنب قراءة نفس الرسالة مرتين
            const payloadStr = message[1][1]; // استخراج النص المرتبط بمفتاح 'payload'
            
            // تحويل النص إلى كائن يطابق العقد (Contract)
            const data: TimingContract = JSON.parse(payloadStr);

            // تمرير البيانات للدالة المطلوبة
            callback(data, lastId);
          }
        }
      } catch (error) {
        console.error('❌ [Consumer Error] فشل في قراءة المجرى:', error);
        // انتظار ثانية قبل إعادة المحاولة في حال انقطاع الاتصال
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
  }
}
