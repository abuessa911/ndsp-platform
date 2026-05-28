import unittest

from app.core.data.unified_market_router import (
    UnifiedAssetClass,
    UnifiedProviderName,
    UnifiedMarketRecord,
    UnifiedMarketRouter,
    is_crypto_symbol,
    market_record_to_dict,
    resolve_unified_asset_class,
)


class TestUnifiedMarketRouter(unittest.TestCase):
    def test_crypto_detection(self):
        self.assertTrue(is_crypto_symbol("BTCUSDT"))
        self.assertTrue(is_crypto_symbol("ETHUSDT"))
        self.assertFalse(is_crypto_symbol("EURUSD"))
        self.assertFalse(is_crypto_symbol("XAUUSD"))

    def test_route_selection(self):
        router = UnifiedMarketRouter()
        self.assertEqual(router.route_name("BTCUSDT"), UnifiedProviderName.BINANCE)
        self.assertEqual(router.route_name("EURUSD"), UnifiedProviderName.GLOBAL)
        self.assertEqual(router.route_name("XAUUSD"), UnifiedProviderName.GLOBAL)
        self.assertEqual(router.route_name("USOIL"), UnifiedProviderName.GLOBAL)

    def test_asset_class_resolution(self):
        self.assertEqual(resolve_unified_asset_class("BTCUSDT"), UnifiedAssetClass.CRYPTO)
        self.assertEqual(resolve_unified_asset_class("EURUSD"), UnifiedAssetClass.FOREX)
        self.assertEqual(resolve_unified_asset_class("XAUUSD"), UnifiedAssetClass.METALS)
        self.assertEqual(resolve_unified_asset_class("USOIL"), UnifiedAssetClass.ENERGY)
        self.assertEqual(resolve_unified_asset_class("US30"), UnifiedAssetClass.INDEX)

    def test_record_contract_no_execution(self):
        record = UnifiedMarketRecord(
            symbol="BTCUSDT",
            requested_symbol="BTCUSDT",
            asset_class=UnifiedAssetClass.CRYPTO,
            price=100.0,
            source="unit_test",
            provider_route="binance_spot",
            timestamp_ms=1,
            utc_time="2026-01-01T00:00:00+00:00",
            status="HEALTHY",
            context_only=True,
            execution_allowed=False,
            raw={},
        )

        self.assertTrue(record.context_only)
        self.assertFalse(record.execution_allowed)

    def test_record_to_dict(self):
        record = UnifiedMarketRecord(
            symbol="EURUSD",
            requested_symbol="EURUSD",
            asset_class=UnifiedAssetClass.FOREX,
            price=1.1,
            source="unit_test",
            provider_route="global_provider",
            timestamp_ms=1,
            utc_time="2026-01-01T00:00:00+00:00",
            status="HEALTHY",
            context_only=True,
            execution_allowed=False,
            raw={},
        )

        data = market_record_to_dict(record)

        self.assertEqual(data["asset_class"], "forex")
        self.assertEqual(data["execution_allowed"], False)
        self.assertEqual(data["context_only"], True)

    def test_record_to_dict_none(self):
        self.assertIsNone(market_record_to_dict(None))


if __name__ == "__main__":
    unittest.main()
