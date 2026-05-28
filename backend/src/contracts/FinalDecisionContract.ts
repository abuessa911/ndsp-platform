export interface FinalDecisionContract {
  // 1. بيانات الاتجاه (مسموح بها فقط من طبقة Dominant Timed Direction)
  direction: 'bullish' | 'bearish' | 'neutral';
  direction_authority: string;
  direction_source: string;
  timing_controller: 'L&M' | 'S';

  // 2. بيانات الثقة والجودة (مسموح بها فقط من طبقة Decision Quality Stack)
  confidence: number;
  confidence_source: string;
  quality_score: number;
  grade: 'A' | 'B' | 'C' | 'D' | 'F';
  quality_label: string;

  // 3. بيانات المخاطر (مسموح بها من Risk State و Black Layer)
  risk_state: 'normal' | 'caution' | 'market_closed' | 'danger_block';
  
  // 4. حالة التنفيذ (مسموح بها من Governance Runtime)
  decision_state: 'active' | 'active_caution' | 'blocked';
  execution_allowed: boolean;
  execution_mode: 'decision_support_only' | 'live_execution';
}
