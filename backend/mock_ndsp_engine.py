import redis
import json
import time
import random
from datetime import datetime

# إعداد الاتصال بخادم Redis (تأكد من أن Redis يعمل لديك)
# إذا كان Redis على خادم مختلف، قم بتغيير localhost إلى عنوان الـ IP
try:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.ping()
    print("✅ متصل بخادم Redis بنجاح!")
except Exception as e:
    print(f"❌ فشل الاتصال بخادم Redis: {e}")
    exit(1)

# اسم الـ Stream الذي يستمع إليه WebSocket Bridge
# (يجب أن يتطابق مع قيمة NDSP_STREAMS.DECISION في ملف websocketServer.ts)
STREAM_KEY = 'ndsp:stream:decision'

SYMBOLS = ['BTC/USD', 'ETH/USD', 'EUR/USD', 'XAU/USD', 'AAPL', 'NDX']
DIRECTIONS = ['bullish', 'bearish', 'neutral']
GRADES = ['A', 'B', 'C', 'D']
CONTROLLERS = ['VWAP Crossover', 'Momentum Surge', 'Orderbook Imbalance', 'Mean Reversion']
RISK_STATES = ['normal', 'normal', 'elevated', 'extreme'] # تكرار normal لزيادة احتماليته

def generate_and_send_decision():
    print(f"🚀 بدء تشغيل محرك الاختبار NDSP. جاري إرسال البيانات إلى Stream: {STREAM_KEY}...")
    
    try:
        while True:
            # توليد قرار عشوائي
            symbol = random.choice(SYMBOLS)
            direction = random.choice(DIRECTIONS)
            confidence = random.randint(45, 98)
            grade = random.choice(GRADES)
            execution_allowed = confidence > 70 and grade in ['A', 'B']
            
            decision_data = {
                "decision": {
                    "symbol": symbol,
                    "direction": direction,
                    "confidence": confidence,
                    "grade": grade,
                    "timing_controller": random.choice(CONTROLLERS),
                    "risk_state": random.choice(RISK_STATES),
                    "execution_allowed": execution_allowed,
                    "execution_mode": "Auto_Market" if execution_allowed else "Blocked_By_Risk",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            # تحويل القاموس إلى نص JSON
            payload = json.dumps(decision_data)
            
            # إرسال البيانات إلى Redis Stream
            # نستخدم xadd مع '*' ليقوم Redis بتوليد ID تلقائي للحدث
            event_id = r.xadd(STREAM_KEY, {'payload': payload})
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 📡 تم إرسال قرار لـ {symbol} | ID: {event_id}")
            
            # انتظار مدة عشوائية بين 2 إلى 8 ثواني قبل إرسال القرار التالي
            sleep_time = random.uniform(2.0, 8.0)
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف محرك الاختبار.")

if __name__ == "__main__":
    generate_and_send_decision()
