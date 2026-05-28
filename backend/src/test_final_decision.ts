import { FinalDecisionAggregator } from './eventbus/aggregators/FinalDecisionAggregator';

console.log("🚀 جاري محاكاة تجميع القرار النهائي (Final Decision Aggregation)...");

// محاكاة بيانات قادمة من الطبقات السابقة بعد معالجتها
const mockDirection = {
  direction: 'bullish',
  authority: 'Dominant Timed Direction',
  source: 'weekly.lm_direction',
  timing_controller: 'L&M'
};

const mockQuality = {
  confidence: 82,
  source: 'Decision Quality Stack',
  quality_score: 8.5,
  grade: 'A',
  label: 'High Conviction'
};

const mockRisk = {
  state: 'normal'
};

const mockGovernance = {
  decision_state: 'active',
  execution_allowed: false, // ممنوع التنفيذ المباشر
  execution_mode: 'decision_support_only'
};

async function runTest() {
  const eventId = await FinalDecisionAggregator.aggregateAndPublish(
    mockDirection,
    mockQuality,
    mockRisk,
    mockGovernance
  );

  if (eventId) {
    console.log("\n📊 [القرار النهائي المعتمد والمطابق للعقد]:");
    console.log(`- 🧭 الاتجاه: ${mockDirection.direction} (المصدر: ${mockDirection.source})`);
    console.log(`- 📈 الثقة: ${mockQuality.confidence}% (التقييم: ${mockQuality.grade})`);
    console.log(`- 🛡️ حالة المخاطرة: ${mockRisk.state}`);
    console.log(`- ⚖️ حالة التنفيذ: ${mockGovernance.execution_mode}\n`);
  }
  process.exit(0);
}

runTest();
