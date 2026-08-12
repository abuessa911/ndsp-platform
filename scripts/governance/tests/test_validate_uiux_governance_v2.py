#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "scripts/governance/validate_uiux_governance_v2.py"
POLICY_PATH = (
    ROOT
    / "docs/99-governance/ui-architecture/"
    / "NDSP_UIUX_GOVERNANCE_SUPERSESSION_V2.yaml"
)

spec = importlib.util.spec_from_file_location("ndsp_uiux_v2_validator", MODULE_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)


class V2GovernanceValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy_context = validator.Context()
        self.policy = validator.load_yaml(POLICY_PATH, self.policy_context)
        (
            self.approved_names,
            self.generic_labels,
            self.private_filenames,
        ) = validator.validate_v2_policy(
            self.policy,
            self.policy_context,
        )
        self.forbidden_tokens = {
            str(item).strip()
            for item in validator.sequence(
                validator.mapping(self.policy.get("confidentiality")).get(
                    "forbidden_customer_disclosure"
                )
            )
            if str(item).strip()
        }

    def test_repository_v2_policy_is_valid(self) -> None:
        self.assertEqual([], self.policy_context.errors)

    def test_sixth_customer_visible_name_is_rejected(self) -> None:
        policy = copy.deepcopy(self.policy)
        exposure = policy["customer_terminology_exposure"]
        exposure["maximum_approved_named_items"] = 6
        exposure["approved_customer_visible_names"].append("Secret Sixth Name")
        context = validator.Context()
        validator.validate_v2_policy(policy, context)
        rule_ids = {item.rule_id for item in context.errors}
        self.assertIn("CUSTOMER_VISIBLE_NAME_LIMIT_INVALID", rule_ids)
        self.assertIn("CUSTOMER_VISIBLE_ALLOWLIST_DRIFT", rule_ids)

    def test_legacy_primary_brand_is_rejected(self) -> None:
        policy = copy.deepcopy(self.policy)
        policy["visual_identity"]["indigo_violet_primary_brand_accent"] = True
        context = validator.Context()
        validator.validate_v2_policy(policy, context)
        self.assertIn(
            "LEGACY_PRIMARY_BRAND_REINTRODUCED",
            {item.rule_id for item in context.errors},
        )

    def test_confidential_master_artifact_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            leaked = repo / self.private_filenames[0]
            leaked.write_text("confidential", encoding="utf-8")
            context = validator.Context()
            validator.enforce_private_artifact_absence(
                repo,
                self.private_filenames,
                context,
            )
            self.assertIn(
                "CONFIDENTIAL_MASTER_COMMITTED_TO_PUBLIC_REPO",
                {item.rule_id for item in context.errors},
            )

    def test_changed_public_ui_rejects_sixth_name_and_secret_field(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            full = root / "frontend/public-landing/src/example.tsx"
            full.parent.mkdir(parents=True)
            full.write_text(
                """const customerVisibleNames = [
"TDL",
"NMP",
"Nawaf Golden Signal",
"Enhanced Nawaf Golden Signal",
"Devil's Advocate",
"Secret Sixth Name"
];
const payload = {"internal_state": source};
""",
                encoding="utf-8",
            )
            context = validator.Context()
            validator.scan_source_file(
                Path("frontend/public-landing/src/example.tsx"),
                full,
                self.approved_names,
                self.generic_labels,
                self.forbidden_tokens,
                context,
            )
            rule_ids = {item.rule_id for item in context.errors}
            self.assertIn("CUSTOMER_VISIBLE_LIST_EXCEEDS_FIVE", rule_ids)
            self.assertIn("UNAPPROVED_CUSTOMER_VISIBLE_NAME", rule_ids)
            self.assertIn(
                "CONFIDENTIAL_FIELD_IN_CUSTOMER_OR_PUBLIC_API",
                rule_ids,
            )

    def test_changed_public_api_rejects_raw_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            full = root / "backend/public_api.py"
            full.parent.mkdir(parents=True)
            full.write_text(
                '@app.get("/api/public/summary")\n'
                'def summary():\n'
                '    return {"raw_values": data}\n',
                encoding="utf-8",
            )
            context = validator.Context()
            validator.scan_source_file(
                Path("backend/public_api.py"),
                full,
                self.approved_names,
                self.generic_labels,
                self.forbidden_tokens,
                context,
            )
            self.assertIn(
                "CONFIDENTIAL_FIELD_IN_CUSTOMER_OR_PUBLIC_API",
                {item.rule_id for item in context.errors},
            )

    def test_changed_ui_rejects_legacy_primary_violet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            full = root / "frontend/public-landing/src/theme.ts"
            full.parent.mkdir(parents=True)
            full.write_text(
                'export const theme = { primaryBrand: "violet" };\n',
                encoding="utf-8",
            )
            context = validator.Context()
            validator.scan_source_file(
                Path("frontend/public-landing/src/theme.ts"),
                full,
                self.approved_names,
                self.generic_labels,
                self.forbidden_tokens,
                context,
            )
            self.assertIn(
                "LEGACY_PRIMARY_BRAND_COLOR_IN_CHANGED_UI",
                {item.rule_id for item in context.errors},
            )

    def test_approved_five_names_and_gold_primary_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            full = root / "frontend/public-landing/src/safe.ts"
            full.parent.mkdir(parents=True)
            full.write_text(
                """const customerVisibleNames = [
"TDL",
"NMP",
"Nawaf Golden Signal",
"Enhanced Nawaf Golden Signal",
"Devil's Advocate"
];
export const theme = { primaryBrand: "gold" };
""",
                encoding="utf-8",
            )
            context = validator.Context()
            validator.scan_source_file(
                Path("frontend/public-landing/src/safe.ts"),
                full,
                self.approved_names,
                self.generic_labels,
                self.forbidden_tokens,
                context,
            )
            self.assertEqual([], context.errors)


if __name__ == "__main__":
    unittest.main()
