import json, tempfile, unittest
from pathlib import Path
from backend.layers.canonical_v1.registry_lock import EXPECTED_IDS, validate_registry_lock

class TestRegistryLock(unittest.TestCase):
    def test_official_registry_has_all_16_layers(self):
        root = Path(__file__).resolve().parents[1]
        registry = Path(__file__).resolve().parents[4] / "docs/03-contracts/NDSP_16_LAYER_CORE_REGISTRY_V1.json"
        result = validate_registry_lock(registry, root)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["ids"], EXPECTED_IDS)
        self.assertEqual(result["layer_count"], 16)

    def test_missing_layer_is_rejected(self):
        root = Path(__file__).resolve().parents[1]
        official = Path(__file__).resolve().parents[4] / "docs/03-contracts/NDSP_16_LAYER_CORE_REGISTRY_V1.json"
        data = json.loads(official.read_text(encoding="utf-8"))
        data["layers"] = [x for x in data["layers"] if x["id"] != "NDSP-CORE-L07"]
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)/"registry.json"
            p.write_text(json.dumps(data),encoding="utf-8")
            result = validate_registry_lock(p,root)
        self.assertFalse(result["ok"])

    def test_missing_registry_is_rejected(self):
        root = Path(__file__).resolve().parents[1]
        result = validate_registry_lock(
            root / "missing-registry.json",
            root,
        )
        self.assertFalse(result["ok"])
        self.assertTrue(
            result["errors"][0].startswith("REGISTRY_NOT_FOUND:")
        )

    def test_invalid_json_is_rejected(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "registry.json"
            p.write_text("{invalid", encoding="utf-8")
            result = validate_registry_lock(p, root)

        self.assertFalse(result["ok"])
        self.assertTrue(
            result["errors"][0].startswith("REGISTRY_INVALID_JSON:")
        )

    def test_invalid_top_level_schema_is_rejected(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "registry.json"
            p.write_text("[]", encoding="utf-8")
            result = validate_registry_lock(p, root)

        self.assertFalse(result["ok"])
        self.assertEqual(
            result["errors"],
            ["REGISTRY_INVALID_SCHEMA: top level must be an object"],
        )

    def test_missing_canonical_name_is_rejected(self):
        root = Path(__file__).resolve().parents[1]
        official = (
            Path(__file__).resolve().parents[4]
            / "docs/03-contracts/NDSP_16_LAYER_CORE_REGISTRY_V1.json"
        )
        data = json.loads(official.read_text(encoding="utf-8"))
        data["layers"][0]["canonical_name"] = ""

        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "registry.json"
            p.write_text(json.dumps(data), encoding="utf-8")
            result = validate_registry_lock(p, root)

        self.assertFalse(result["ok"])
        self.assertIn(
            "canonical_name values must be non-empty strings",
            result["errors"],
        )

if __name__ == "__main__":
    unittest.main()
