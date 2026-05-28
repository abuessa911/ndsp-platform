import { telegramNotifier } from '../packages/notifications/src/telegram';

async function runTest() {
  console.log("🚀 Starting NDSP Multi-Channel Broadcast Test...");
  
  await telegramNotifier.sendAlert(
    "NDSP Engine initialization successful. Pro, Elite, and SaaS channels are now linked.",
    "INFO"
  );
  
  console.log("🏁 Test finished check your Telegram channels!");
}

runTest();
