import unittest

from app.core.data.binance_live import OhlcvRecord, validate_ohlcv_record


class TestBinanceLiveAdapter(unittest.TestCase):
    def test_validate_good_ohlcv(self):
        record = OhlcvRecord(
            symbol="BTCUSDT",
            interval="1h",
            timestamp=1,
            open_time_utc="2026-01-01T00:00:00+00:00",
            open=100.0,
            high=110.0,
            low=90.0,
            close=105.0,
            volume=10.0,
            close_time=2,
        )
        self.assertTrue(validate_ohlcv_record(record))

    def test_validate_bad_ohlcv(self):
        record = OhlcvRecord(
            symbol="BTCUSDT",
            interval="1h",
            timestamp=1,
            open_time_utc="2026-01-01T00:00:00+00:00",
            open=100.0,
            high=95.0,
            low=90.0,
            close=105.0,
            volume=10.0,
            close_time=2,
        )
        self.assertFalse(validate_ohlcv_record(record))


if __name__ == "__main__":
    unittest.main()
