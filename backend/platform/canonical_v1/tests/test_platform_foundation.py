import unittest
from pathlib import Path

from backend.platform.canonical_v1.boundary_lock import validate_architecture_boundaries
from backend.data_foundation.canonical_v1.asset_master_registry import AssetMasterRegistry
from backend.data_foundation.canonical_v1.source_registry import SourceRegistry
from backend.contracts.canonical_v1.contract_registry import ContractRegistry
from backend.data_foundation.canonical_v1.data_quality_gate import evaluate_data_quality
from backend.data_foundation.canonical_v1.provider_reconciliation import reconcile_numeric_observations
from backend.evidence.canonical_v1.decision_ledger import append_record, verify_record
from backend.simulation.canonical_v1.replay import validate_as_of_inputs
from backend.simulation.canonical_v1.scenario import run_scenario
from backend.integrations.canonical_v1.gateway import prepare_external_payload
from backend.commercial.canonical_v1.entitlements import check_entitlement

PROJECT=Path(__file__).resolve().parents[4]
DOCS=PROJECT/"docs/03-contracts"

class TestPlatformFoundation(unittest.TestCase):
    def test_architecture_boundaries(self):
        result=validate_architecture_boundaries(
            DOCS/"NDSP_16_LAYER_CORE_REGISTRY_V1.json",
            DOCS/"NDSP_PLATFORM_CAPABILITY_REGISTRY_V1.json",
        )
        self.assertTrue(result["ok"],result["errors"])
        self.assertEqual(result["layer_count"],16)
        self.assertEqual(result["capability_count"],28)

    def test_asset_aliases_resolve_to_one_identity(self):
        registry=AssetMasterRegistry(DOCS/"NDSP_ASSET_MASTER_REGISTRY_V1.json")
        ids={
            registry.resolve("BTCUSD")["internal_asset_id"],
            registry.resolve("BTCUSDT","binance")["internal_asset_id"],
            registry.resolve("BTC-USD","coinbase")["internal_asset_id"],
            registry.resolve("XBTUSD","kraken")["internal_asset_id"],
        }
        self.assertEqual(ids,{"NDSP:CRYPTO:BTC:USD"})

    def test_unknown_asset_fails_closed(self):
        registry=AssetMasterRegistry(DOCS/"NDSP_ASSET_MASTER_REGISTRY_V1.json")
        result=registry.resolve("NOTAREALASSET")
        self.assertFalse(result["decision_use_allowed"])

    def test_contract_source_and_quality_gate(self):
        asset=AssetMasterRegistry(DOCS/"NDSP_ASSET_MASTER_REGISTRY_V1.json").resolve("ETHUSDT")
        source=SourceRegistry(DOCS/"NDSP_SOURCE_REGISTRY_V1.json").get("TWELVEDATA_MARKET_DATA")
        contract=ContractRegistry(DOCS/"NDSP_SCHEMA_CONTRACT_REGISTRY_V1.json").require(
            "NDSP-CONTRACT-CANONICAL-SNAPSHOT","1.0.0"
        )
        result=evaluate_data_quality(
            asset_identity=asset,source_identity=source,contract_status=contract,
            freshness_status="CURRENT",completeness=True,integrity=True,
        )
        self.assertTrue(result["decision_use_allowed"])

    def test_reconciliation_detects_conflict(self):
        result=reconcile_numeric_observations([
            {"source_id":"A","authority_rank":1,"value":100},
            {"source_id":"B","authority_rank":2,"value":105},
        ],tolerance_ratio=0.01)
        self.assertEqual(result["status"],"SOURCE_CONFLICT")
        self.assertFalse(result["decision_use_allowed"])

    def test_ledger_tamper_detection(self):
        record=append_record(payload={"decision_id":"D1","state":"READY"})
        self.assertTrue(verify_record(record))
        record["payload"]["state"]="BLOCKED"
        self.assertFalse(verify_record(record))

    def test_replay_blocks_future_evidence(self):
        result=validate_as_of_inputs(
            as_of="2026-01-01T00:00:00+00:00",
            evidence_timestamps=["2026-01-02T00:00:00+00:00"],
        )
        self.assertEqual(result["status"],"LOOK_AHEAD_BIAS_BLOCKED")

    def test_simulation_never_publishes_live(self):
        result=run_scenario(base_decision_id="D1",assumptions={},computed_outputs={})
        self.assertFalse(result["decision_publish_allowed"])
        self.assertEqual(result["state"],"SIMULATION_ONLY")

    def test_gateway_has_no_decision_logic(self):
        result=prepare_external_payload({"decision_id":"D1","private_equations":"secret"})
        self.assertNotIn("private_equations",result)
        self.assertFalse(result["decision_logic_executed_in_gateway"])

    def test_billing_never_changes_decision(self):
        result=check_entitlement(plan="premium",feature="advanced_report")
        self.assertTrue(result["allowed"])
        self.assertFalse(result["changes_decision"])

if __name__=="__main__":
    unittest.main()
