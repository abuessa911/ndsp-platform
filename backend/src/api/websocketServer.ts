import { Server } from 'socket.io';
import { createServer } from 'http';
import express from 'express';
import cors from 'cors';
import { redis, NDSP_STREAMS } from '../eventbus/redisClient';

const app = express();
app.use(cors());

const httpServer = createServer(app);

// إعداد خادم WebSockets مع السماح بالاتصال من الواجهة
const io = new Server(httpServer, {
cors: {
origin: "*", // في الإنتاج، قم بتحديد رابط الـ Frontend الخاص بك
methods: ["GET", "POST"]
}
});

io.on('connection', (socket) => {
console.log([Frontend Bridge] Client connected: ${socket.id});

socket.on('disconnect', () => {
console.log([Frontend Bridge] Client disconnected: ${socket.id});
});
});

// دالة للاستماع لقرارات NDSP وبثها للواجهة
async function broadcastDecisions() {
let lastId = '$';
console.log([WebSocket Broadcaster] Listening to ${NDSP_STREAMS.DECISION} to broadcast...);

while (true) {
try {
const streamResult = await redis.xread(
'BLOCK', 0,
'STREAMS', NDSP_STREAMS.DECISION, lastId
);

  if (streamResult) {
    const messages = streamResult[0][1];
    for (const message of messages) {
      lastId = message[0];
      const payloadStr = message[1][1]; 
      
      // بث القرار مباشرة لكل المستخدمين المتصلين
      io.emit('ndsp_final_decision', {
        eventId: lastId,
        data: JSON.parse(payloadStr)
      });
      
      console.log(`[WebSocket] Broadcasted Decision ${lastId} to Frontend.`);
    }
  }
} catch (error) {
  console.error('[WebSocket Error] Failed to read stream:', error);
  await new Promise(resolve => setTimeout(resolve, 5000));
}


}
}

const PORT = process.env.PORT || 3001;
httpServer.listen(PORT, () => {
console.log([API Gateway] WebSocket Server is running on port ${PORT});
broadcastDecisions(); // بدء الاستماع والبث
});
