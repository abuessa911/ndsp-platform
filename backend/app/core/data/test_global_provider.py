import unittest

from app.core.data.global_provider import (
    GlobalDataProvider,
    MarketAssetClass,
    MarketDataRecord,
    MarketRouter,
    record_to_dict,
)


class TestGlobalProvider(unittest.TestCase):
    def test_router_gold(self):
        self.assertEqual(MarketRouter.twelve_symbol("GOLD"), "XAU/USD")
        self.assertEqual(MarketRouter.yahoo_symbol("GOLD"), "GC=F")
        self.assertEqual(MarketRouter.asset_class("GOLD"), MarketAssetClass.METALS)

    def test_router_forex(self):
        self.assertEqual(MarketRouter.twelve_symbol("EURUSD"), "EUR/USD")
        self.assertEqual(MarketRouter.yahoo_symbol("EURUSD"), "EURUSD=X")
        self.assertEqual(MarketRouter.asset_class("EURUSD"), MarketAssetClass.FOREX)

    def test_router_indices(self):
        self.assertEqual(MarketRouter.yahoo_symbol("US30"), "^DJI")
        self.assertEqual(MarketRouter.asset_class("US30"), MarketAssetClass.INDEX)

    def test_format_output(self):
        provider = GlobalDataProvider(api_key="")
        record = provider._format_output(
            symbol="GOLD",
            provider_symbol="GC=F",
            price=2400.50,
            source="unit_test",
            raw={"x": 1},
        )

        self.assertEqual(record.symbol, "GOLD")
        self.assertEqual(record.asset_class, MarketAssetClass.METALS)
        self.assertEqual(record.price, 2400.50)
        self.assertEqual(record.source, "unit_test")
        self.assertEqual(record.status, "HEALTHY")

    def test_record_to_dict(self):
        provider = GlobalDataProvider(api_key="")
        record = provider._format_output(
            symbol="EURUSD",
            provider_symbol="EURUSD=X",
            price=1.0812,
            source="unit_test",
            raw={},
        )

        d = record_to_dict(record)

        self.assertIsNotNone(d)
        self.assertEqual(d["asset_class"], "forex")
        self.assertEqual(d["price"], 1.0812)

    def test_record_to_dict_none(self):
        self.assertIsNone(record_to_dict(None))

    def test_market_data_record_contract(self):
        record = MarketDataRecord(
            symbol="US30",
            provider_symbol="^DJI",
            asset_class=MarketAssetClass.INDEX,
            price=39000.0,
            timestamp_ms=1,
            utc_time="2026-01-01T00:00:00+00:00",
            source="unit_test",
            status="HEALTHY",
            raw={},
        )

        self.assertEqual(record.symbol, "US30")
        self.assertEqual(record.asset_class.value, "index")


if __name__ == "__main__":
    unittest.main()
