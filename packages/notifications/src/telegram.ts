import axios from 'axios';

export class TelegramNotifier {
  private botToken: string;
  private chatIds: string[]; 
  private telegramApiUrl: string;

  constructor() {
    this.botToken = process.env.TELEGRAM_BOT_TOKEN || '';
    
    const rawChatIds = process.env.TELEGRAM_CHAT_ID || '-1003491841685,-1003793881886,-1003907426334';
    
    this.chatIds = rawChatIds.split(',').map(id => id.trim()).filter(Boolean);
    
    this.telegramApiUrl = `https://api.telegram.org/bot${this.botToken}/sendMessage`;
  }

  /**
   * إرسال تنبيه فوري مبثوق لجميع القنوات (Pro, Elite, SaaS)
   */
  public async sendAlert(message: string, severity: 'INFO' | 'WARNING' | 'CRITICAL' = 'INFO') {
    if (!this.botToken) {
      console.error('Telegram Notifier ERROR: TELEGRAM_BOT_TOKEN is missing from .env file.');
      return;
    }

    if (this.chatIds.length === 0) {
      console.error('Telegram Notifier ERROR: No Chat IDs provided.');
      return;
    }

    const emoji = severity === 'CRITICAL' ? '🚨' : severity === 'WARNING' ? '⚠️' : 'ℹ️';
    
    const formattedMessage = `
${emoji} *NDSP SYSTEM ALERT* ${emoji}
----------------------------------
*Severity:* ${severity}
*Message:* ${message}
*Timestamp:* ${new Date().toISOString()}
----------------------------------
    `;

    // بث الرسالة لكل قناة في نفس الوقت عبر الـ Loop
    for (const chatId of this.chatIds) {
      try {
        await axios.post(this.telegramApiUrl, {
          chat_id: chatId,
          text: formattedMessage,
          parse_mode: 'Markdown',
        });
        console.log(`[Success] Alert broadcasted to channel: ${chatId}`);
      } catch (error: any) {
        console.error(`[Error] Failed to send alert to channel ${chatId}:`, error.response?.data || error.message);
      }
    }
  }
}

export const telegramNotifier = new TelegramNotifier();
