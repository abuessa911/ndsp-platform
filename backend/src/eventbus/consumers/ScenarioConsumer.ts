import { redis, NDSP_STREAMS } from '../redisClient';
import { FinalDecisionContract } from '../../contracts/FinalDecisionContract';

export class ScenarioConsumer {
  static async listenForDecisions() {
    let lastId = '$'; // البدء بالاستماع للأحداث الجديدة فقط
    
    console.log(`🎧 [Layer 16 / Scenario Engine] Listening for finalized decisions on ${NDSP_STREAMS.DECISION}...`);

    while (true) {
      try {
        const streamResult = await redis.xread(
          'BLOCK', 0, 
          'STREAMS', NDSP_STREAMS.DECISION, lastId
        );

        if (streamResult) {
          const [stream] = streamResult;
          const messages = stream[1];

          for (const message of messages) {
            lastId = message[0];
            const payloadStr = message[1][1]; 
            const decision: FinalDecisionContract = JSON.parse(payloadStr);

            this.generateNarrative(decision, lastId);
          }
        }
      } catch (error) {
        console.error('❌ [Scenario Engine Error] Failed to read from decision stream:', error);
        await new Promise(resolve => setTimeout(resolve, 5000));
      }
    }
  }

  private static generateNarrative(decision: FinalDecisionContract, eventId: string) {
    console.log(`\n=================================================`);
    console.log(`📜 [NDSP Scenario & Explainability Report]`);
    console.log(`🔗 Event ID: ${eventId}`);
    console.log(`=================================================`);
    
    // Narrative Logic based on Layer 16 Authority
    if (decision.decision_state === 'blocked') {
        console.log(`🛑 التفسير (Alert): تم حظر الفرصة بسبب حالة المخاطرة (${decision.risk_state}).`);
        console.log(`💡 السياق: رغم أن الاتجاه الهيكلي هو (${decision.direction})، إلا أن نظام الحماية تدخل لمنع أي تحرك.`);
        return;
    }

    let scenarioAction = decision.direction === 'bullish' ? 'تمركز شرائي' : decision.direction === 'bearish' ? 'تمركز بيعي' : 'مراقبة محايدة';
    
    console.log(`🧭 السيناريو الأساسي: يُرجح بناء ${scenarioAction} مدعوم بقراءة من (${decision.direction_source}).`);
    console.log(`📊 قوة السيناريو: مستوى الثقة يُقدر بـ ${decision.confidence}% (تصنيف ${decision.grade}) - [${decision.quality_label}].`);
    
    if (decision.risk_state === 'caution' || decision.decision_state === 'active_caution') {
        console.log(`⚠️ تنبيهات السلوك (Warnings): يُنصح بتقليل حجم المخاطرة أو انتظار تأكيد سعري إضافي بسبب حالة (Caution).`);
    } else {
        console.log(`✅ بيئة التنفيذ: البيئة خالية من الموانع القوية (Risk: ${decision.risk_state}).`);
    }
    
    console.log(`📌 توجيه الحوكمة: ${decision.execution_mode === 'decision_support_only' ? 'دعم قرار للمتداول فقط (لا يوجد تنفيذ آلي).' : 'مسموح بالتنفيذ الآلي.'}`);
    console.log(`=================================================\n`);
  }
}
