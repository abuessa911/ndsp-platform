/**
 * Layer 12 & 14: Black Layer & Governance Runtime
 * الصلاحية: رفع مستوى الخطر، حظر التنفيذ، وتحويل حالة القرار إلى Blocked.
 * الممنوعات: تغيير الاتجاه (يبقى الاتجاه محفوظاً كسياق حتى لو كان السوق مغلقاً).
 */
export interface GovernanceContract {
  risk_state: 'normal' | 'caution' | 'high_risk' | 'market_closed';
  black_layer_state: 'clear' | 'protective_block' | 'danger_block';
  execution_allowed: boolean; // Must ALWAYS be false in NDSP (Decision Support Only)
  execution_mode: 'decision_support_only';
  decision_state: 'active' | 'active_caution' | 'blocked';
}
