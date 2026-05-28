from __future__ import annotations

QUARANTINED_ROUTE_MARKERS = (
    "signal",
    "trading",
    "trade",
    "execution",
    "executor",
    "paper",
    "live_trader",
    "binance",
    "orderflow",
)

QUARANTINED_FILES = (
    "app/api/routers/signal.py",
    "app/api_execution.py",
    "app/api/execution_learning_api.py",
    "app/api/execution_optimizer_api.py",
    "app/core/execution_filter.py",
    "app/execution/ai_execution_assistant.py",
    "app/execution/binance_executor.py",
    "app/execution/execution_engine.py",
    "app/execution/execution_gate.py",
    "app/execution/execution_learning.py",
    "app/execution/execution_logger.py",
    "app/execution/execution_optimizer.py",
    "app/execution/executor.py",
    "app/execution/live_trader.py",
    "app/execution/paper_executor.py",
    "app/execution/run_trader.py",
    "app/execution/safe_executor.py",
    "app/execution/smart_execution.py",
    "app/execution/smart_execution_v2.py",
    "app/execution/trader.py",
    "app/integrations/market/binance_feed.py",
    "app/integrations/market/market/binance_feed.py",
    "app/services/binance_market.py",
)
