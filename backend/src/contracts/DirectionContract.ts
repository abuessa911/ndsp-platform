/**
 * Layer 6: Dominant Timed Direction
 * الصلاحية: السلطة الوحيدة المخولة بتحديد الاتجاه النهائي للقرار.
 * الممنوعات: استقبال تأثيرات الزخم أو الأخبار لتعديل الاتجاه.
 */
export interface DominantDirectionContract {
  direction: 'bullish' | 'bearish' | 'neutral';
  source: string;
  controller: 'L&M' | 'S';
}
