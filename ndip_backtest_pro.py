import pandas as pd
import vectorbt as vbt

print("\n====== BACKTEST RESULTS ======\n")

# =========================
# إعدادات
# =========================
SYMBOL = "BTC-USD"
START = "2023-01-01"   # 👈 مهم: داخل آخر سنتين
INTERVAL = "1h"

# =========================
# تحميل البيانات
# =========================
data = vbt.YFData.download(
    SYMBOL,
    start=START,
    interval=INTERVAL
)

price = data.get("Close")

# =========================
# حماية من البيانات الفاضية
# =========================
if price is None or price.empty:
    raise ValueError("❌ مافي بيانات — غير الفترة أو المصدر")

# =========================
# تنظيف البيانات
# =========================
price.index = pd.to_datetime(price.index)
price = price.asfreq("1h")
price = price.ffill()

# =========================
# الاستراتيجية
# =========================
fast_ma = price.rolling(10).mean()
slow_ma = price.rolling(50).mean()

entries = fast_ma > slow_ma
exits = fast_ma < slow_ma

# =========================
# الباكتيست
# =========================
portfolio = vbt.Portfolio.from_signals(
    close=price,
    entries=entries,
    exits=exits,
    fees=0.001,
    slippage=0.001,
    freq="1h",
    init_cash=10000
)

# =========================
# النتائج
# =========================
stats = portfolio.stats()
print(stats)

print("\n====== EXTRA METRICS ======\n")
print(f"Total Return: {portfolio.total_return() * 100:.2f}%")
print(f"Max Drawdown: {portfolio.max_drawdown() * 100:.2f}%")
print(f"Win Rate: {portfolio.trades.win_rate() * 100:.2f}%")
print(f"Total Trades: {portfolio.trades.count()}")

portfolio.plot().show()
