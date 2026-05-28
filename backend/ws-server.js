const WebSocket = require("ws");

// مهم: فتح الاتصال لكل الشبكات
const wss = new WebSocket.Server({
  port: 8080,
  host: "0.0.0.0"
});

console.log("NDSP WS SERVER RUNNING ON 0.0.0.0:8080");

function generateMarket() {
  return {
    asset: "BTCUSDT",
    price: 100 + Math.random() * 100,
    volatility: Math.random(),
    liquidity: Math.random(),
    timestamp: Date.now()
  };
}

function generateDecision(market) {
  const risk =
    market.volatility > 0.7 ? "HIGH" :
    market.volatility > 0.4 ? "MEDIUM" :
    "LOW";

  return {
    asset: market.asset,
    risk,
    decision: market.price > 120 ? "SELL" : "BUY",
    confidence: Math.min(0.95, market.liquidity + (1 - market.volatility))
  };
}

setInterval(() => {
  const market = generateMarket();
  const decision = generateDecision(market);

  const payload = JSON.stringify({
    type: "NDSP_UPDATE",
    market,
    decision
  });

  wss.clients.forEach((client) => {
    if (client.readyState === 1) {
      client.send(payload);
    }
  });
}, 2000);
