/**
 * Layer 13: Decision Quality Stack
 * الصلاحية: تجميع تأثيرات الطبقات (NMP, Momentum, Divergence, Golden Alignment) لإنتاج الثقة.
 * الممنوعات: ممنوع احتوائها على حقل الاتجاه (Direction) أو تعديله.
 */
export interface DecisionQualityContract {
  final_confidence: number; // 0 to 100
  quality_score: number;
  grade: 'A' | 'B' | 'C' | 'D' | 'F';
  quality_label: string;
  golden_alignment_active: boolean;
}
