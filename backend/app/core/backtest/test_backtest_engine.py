import unittest

from app.core.backtest.backtest_engine import BacktestEngine


class TestBacktestEngine(unittest.TestCase):
    def test_backtest_runs_on_mock_data(self):
        engine = BacktestEngine()
        mock_history = [
            {"timestamp": 1, "open": 34000, "high": 35200, "low": 33900, "close": 35000, "symbol": "BTCUSDT"},
            {"timestamp": 2, "open": 35000, "high": 35100, "low": 34400, "close": 34500, "symbol": "BTCUSDT"},
            {"timestamp": 3, "open": 34500, "high": 36100, "low": 34400, "close": 36000, "symbol": "BTCUSDT"},
        ]

        results = engine.run_on_data(mock_history)

        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].simulated_direction, "BULLISH")
        self.assertEqual(results[1].simulated_direction, "BEARISH")
        self.assertFalse(results[0].execution_allowed)

        summary = engine.summarize()
        self.assertEqual(summary["total"], 3)
        self.assertEqual(summary["bullish"], 2)
        self.assertEqual(summary["bearish"], 1)

    def test_backtest_blocks_when_black_layer_blocks(self):
        engine = BacktestEngine()
        mock_history = [
            {"timestamp": 1, "open": 100, "high": 110, "low": 90, "close": 105, "symbol": "BTCUSDT"},
        ]

        results = engine.run_on_data(
            mock_history,
            black_layer_penalty=1.0,
            black_severity="KILL",
        )

        self.assertEqual(results[0].decision_state, "blocked")
        self.assertEqual(results[0].grade, "F_BLOCKED")
        self.assertEqual(results[0].confidence, 0.0)
        self.assertFalse(results[0].execution_allowed)

    def test_backtest_rejects_invalid_ohlc(self):
        engine = BacktestEngine()
        bad_history = [
            {"timestamp": 1, "open": 100, "high": 90, "low": 95, "close": 105, "symbol": "BTCUSDT"},
        ]

        with self.assertRaises(ValueError):
            engine.run_on_data(bad_history)


if __name__ == "__main__":
    unittest.main()
