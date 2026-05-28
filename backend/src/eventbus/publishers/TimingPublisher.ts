import { redis, NDSP_STREAMS } from '../redisClient';
import { TimingContract } from '../../contracts/TimingContract';

export class TimingPublisher {
  /**
   * ضخ قرار التوقيت في مجرى الأحداث
   * @param data بيانات التوقيت المطابقة للعقد الصارم
   */
  static async publish(data: TimingContract): Promise<string> {
    try {
      // استخدام XADD لإضافة الحدث في الـ Stream
      // '*' تعني أن Redis سيقوم بتوليد معرف (ID) زمني فريد للحدث
      const eventId = await redis.xadd(
        NDSP_STREAMS.TIMING,
        '*',
        'payload',
        JSON.stringify(data),
        'timestamp',
        Date.now().toString()
      );

      console.log(`[Layer 3: Timing Authority] ⏱️ Event Published to ${NDSP_STREAMS.TIMING} | ID: ${eventId}`);
      return eventId;
    } catch (error) {
      console.error(`[Layer 3: Timing Authority] ❌ Failed to publish event:`, error);
      throw error;
    }
  }
}
