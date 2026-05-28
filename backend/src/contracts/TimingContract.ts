/**
 * Layer 3: Timing Authority
 * الصلاحية: تحديد المسيطر الزمني فقط.
 * الممنوعات: حساب الاتجاه أو تعديل الثقة.
 */
export interface TimingContract {
  controller: 'L&M' | 'S';
  direction_source: string;
  day_group: 'Monday' | 'Tuesday' | 'Wednesday' | 'Thursday' | 'Friday' | 'Saturday' | 'Sunday';
  decision_authority: string;
}
