import { redis, NDSP_STREAMS } from '../redisClient';
import { FinalDecisionContract } from '../../contracts/FinalDecisionContract';

export class FinalDecisionAggregator {
  /**
   * تجميع القرار النهائي بناءً على وثيقة الحوكمة (Layer 15)
   * Final Decision لا يفكر. Final Decision يجمع.
   */
  static async aggregateAndPublish(
    directionData: any, // من Dominant Timed Direction
    qualityData: any,   // من Decision Quality Stack
    riskData: any,      // من Risk / Black Layer
    governanceData: any // من Governance Runtime
  ): Promise<string | null> {

    // بناء العقد النهائي
    const finalDecision: FinalDecisionContract = {
      // 1. الاتجاه
      direction: directionData.direction,
      direction_authority: directionData.authority,
      direction_source: directionData.source,
      timing_controller: directionData.timing_controller,

      // 2. الثقة والجودة
      confidence: qualityData.confidence,
      confidence_source: qualityData.source,
      quality_score: qualityData.quality_score,
      grade: qualityData.grade,
      quality_label: qualityData.label,

      // 3. المخاطر
      risk_state: riskData.state,

      // 4. الحوكمة
      decision_state: governanceData.decision_state,
      execution_allowed: governanceData.execution_allowed,
      execution_mode: governanceData.execution_mode,
    };

    // تطبيق حوكمة NDSP الصارمة: لا تنفيذ مباشر (Decision Support Only)
    if (finalDecision.execution_allowed === true && finalDecision.execution_mode !== 'decision_support_only') {
       console.warn("⚠️ [Governance Alert] محاولة تمرير قرار تنفيذ مباشر! تم التدخل لفرض وضع دعم القرار (Decision Support Only).");
       finalDecision.execution_allowed = false;
       finalDecision.execution_mode = 'decision_support_only';
    }

    try {
      // ضخ القرار النهائي في المجرى الرسمي للقرارات
      const eventId = await redis.xadd(
        NDSP_STREAMS.DECISION,
        '*', // ID تلقائي من Redis
        'payload',
        JSON.stringify(finalDecision)
      );
      console.log(`✅ [Layer 15 / Final Decision] Decision successfully published to ${NDSP_STREAMS.DECISION}. Event ID: ${eventId}`);
      return eventId;
    } catch (error) {
      console.error('❌ [Final Decision Error] Failed to publish decision to stream:', error);
      return null;
    }
  }
}
