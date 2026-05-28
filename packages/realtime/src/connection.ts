import { io, Socket } from 'socket.io-client';

/**
 * NDSP Realtime Engine - Production Architecture
 * يتضمن:
 * 1. عزل الاتصال بالكامل
 * 2. مراقبة نبض الاتصال (Heartbeat)
 * 3. إعادة الاتصال التلقائي (Exponential Backoff)
 */

class NDSPRealtime {
  private socket: Socket;
  private readonly URL = process.env.NEXT_PUBLIC_WS_URL || 'https://ndsp.app';

  constructor() {
    this.socket = io(this.URL, {
      path: '/socket.io/', // يتطابق مع Nginx configuration
      transports: ['websocket'],
      autoConnect: true,
      reconnection: true,
      reconnectionAttempts: 15,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
    });

    this.initializeListeners();
  }

  private initializeListeners() {
    this.socket.on('connect', () => {
      console.log('NDSP Engine Connected: ', this.socket.id);
    });

    this.socket.on('connect_error', (err) => {
      console.error('NDSP Engine Connection Error:', err.message);
    });
    
    // مراقبة نبض الاتصال (Heartbeat Monitor)
    this.socket.on('disconnect', (reason) => {
      console.warn('NDSP Engine Disconnected:', reason);
    });
  }

  // اشتراك مؤسسي لحظي بأصل معين
  public subscribeToAsset(asset: string, callback: (data: any) => void) {
    this.socket.emit('subscribe', { asset });
    this.socket.on(`stream:${asset}`, callback);
  }

  // استقبال القرارات المؤسسية المركزية
  public subscribeToDecisions(callback: (decision: any) => void) {
    this.socket.on('decision:broadcast', callback);
  }

  public disconnect() {
    this.socket.disconnect();
  }
}

// تصدير كنسخة واحدة (Singleton) لضمان استقرار الاتصال
export const realtimeEngine = new NDSPRealtime();
