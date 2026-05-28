import json
import time
import threading
from flask import Flask
from flask_socketio import SocketIO
import redis

app = Flask(__name__)
# السماح للواجهة بالاتصال من أي نطاق (CORS)
socketio = SocketIO(app, cors_allowed_origins="*")

# إعداد اتصال Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
STREAM_NAME = 'ndsp.decision.stream'

@socketio.on('connect')
def handle_connect():
    print("🟢 [Frontend Bridge] Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("🔴 [Frontend Bridge] Client disconnected")

def broadcast_decisions():
    print(f"📡 [WebSocket Broadcaster] Listening to {STREAM_NAME} to broadcast...")
    last_id = '$' # الاستماع للأحداث الجديدة فقط
    
    while True:
        try:
            # انتظار حدث جديد من Redis
            streams = redis_client.xread({STREAM_NAME: last_id}, count=1, block=5000)
            
            if streams:
                for stream, messages in streams:
                    for message_id, message_data in messages:
                        last_id = message_id
                        payload_str = message_data.get('payload')
                        
                        if payload_str:
                            data = json.loads(payload_str)
                            # بث القرار مباشرة للواجهة
                            socketio.emit('ndsp_final_decision', {
                                'eventId': message_id,
                                'data': data
                            })
                            print(f"➡️ [WebSocket] Broadcasted Decision {message_id} to Frontend.")
        except Exception as e:
            print(f"❌ [WebSocket Error] Failed to read stream: {e}")
            time.sleep(5)

if __name__ == '__main__':
    print("🚀 [API Gateway] WebSocket Server is starting on port 3005...")
    # تشغيل مستمع Redis في مسار (Thread) منفصل لكي لا يوقف الخادم
    threading.Thread(target=broadcast_decisions, daemon=True).start()
    
    # تشغيل خادم WebSockets
    socketio.run(app, host='0.0.0.0', port=3005, debug=False, allow_unsafe_werkzeug=True)
