#!/usr/bin/env python3
"""Validate NDSP UI/UX Governance Supersession V2 and changed-file exposure rules."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    import yaml
except ImportError as exc:
    print("error=Missing dependency: PyYAML")
    print("validation=FAIL")
    print("status=UIUX_GOVERNANCE_V2_INVALID")
    raise SystemExit(1) from exc


DEFAULT_V2_POLICY = Path(
    "docs/99-governance/ui-architecture/"
    "NDSP_UIUX_GOVERNANCE_SUPERSESSION_V2.yaml"
)
DEFAULT_REPORT = Path(
    "docs/99-governance/ui-architecture/"
    "NDSP_UIUX_GOVERNANCE_V2_VALIDATION_REPORT.json"
)

EXPECTED_POLICY_ID = "NDSP-UIUX-GOVERNANCE-SUPERSESSION-V2"
EXPECTED_APPROVED_NAMES = (
    "TDL",
    "NMP",
    "Nawaf Golden Signal",
    "Enhanced Nawaf Golden Signal",
    "Devil's Advocate",
)
EXPECTED_PLANS = ("Free", "Pro", "Elite", "Institutional")
EXPECTED_ENTITLEMENTS = {
    "Free": ("TDL",),
    "Pro": ("TDL", "NMP"),
    "Elite": EXPECTED_APPROVED_NAMES,
    "Institutional": EXPECTED_APPROVED_NAMES,
}
EXPECTED_VISUAL_IDENTITY = {
    "logo_complexity": "3/10",
    "default_foundation": "DEEP_CHARCOAL_NEAR_BLACK",
    "premium_authority_accent": "WARM_REFINED_METALLIC_GOLD",
    "analytical_secondary_accent": "CONTROLLED_SKY_BLUE",
    "high_contrast_neutral": "WHITE_OFF_WHITE",
}
EXPECTED_ARCHITECTURE_INVARIANTS = {
    "one_canonical_cot_dataset": "PRESERVED",
    "decision_layers": "01_TO_16_LOGICAL",
    "capabilities": "01_TO_28_LOGICAL",
    "backend_ownership": "UNCHANGED",
    "database_ownership": "UNCHANGED",
    "service_boundaries": "UNCHANGED",
    "governance_authority": "UNCHANGED",
    "existing_contracts": "PRESERVED",
    "technical_freeze_items": "PRESERVED",
}

SCANNABLE_SUFFIXES = {
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".py", ".json", ".yaml", ".yml", ".html", ".astro",
    ".css", ".scss", ".sass",
}
CUSTOMER_PATH_MARKERS = (
    "/frontend/public-landing/",
    "/frontend/user-portal/",
    "/frontend/ndsp-user-portal",
    "/apps/public-site/",
    "/apps/public-frontend/",
    "/apps/user-portal/",
    "/apps/customer-",
    "/apps/portal/",
)
DESIGN_TOKEN_MARKERS = (
    "/design-system/",
    "/styles/",
    "/theme/",
    "/themes/",
    "/tokens/",
)
EXCLUDED_EXPOSURE_MARKERS = (
    "/docs/",
    "/scripts/",
    "/.github/",
    "/tests/",
    "/test/",
    "/admin-console/",
    "/admin/",
    "/internal/",
)
PUBLIC_API_CONTENT_MARKERS = (
    "/api/public",
    "public_projection",
    "public projection",
    "public api",
    "public_summary",
    "public summary",
)
PRIVATE_MASTER_SUFFIX = "_CONFIDENTIALITY_SUBSCRIPTIONS"

OLD_PRIMARY_BRAND_PATTERN = re.compile(
    r"(?i)(?:(?:primary|brand)[^\n]{0,100}(?:indigo|violet)"
    r"|(?:indigo|violet)[^\n]{0,100}(?:primary|brand))"
)
OLD_PRIMARY_EXEMPT_PATTERN = re.compile(
    r"(?i)\b(?:review|experimental|semantic|status|deprecated|forbidden|"
    r"not\s+primary|no\s+longer|false)\b"
)
DECISION_LAYER_NUMBER_PATTERN = re.compile(
    r"(?i)\bdecision[\s_-]*layer[\s_-]*(?:0?[1-9]|1[0-6])\b"
)
DISPLAY_LIST_PATTERN = re.compile(
    r"""(?is)\b(?:customerVisibleNames|customer_visible_names|
    visibleNames|visible_names|decisionLayerNames|decision_layer_names|
    publicLayerNames|public_layer_names|namedDecisionLayers|
    named_decision_layers)\b\s*[:=]\s*\[(.*?)\]""",
    re.VERBOSE,
)
DISPLAY_SINGLE_PATTERN = re.compile(
    r"""(?ix)\b(?:decisionLayerName|decision_layer_name|
    customerLayerName|customer_layer_name|
    intelligenceLayerName|intelligence_layer_name)\b
    \s*[:=]\s*(?:
        "((?:\\.|[^"\\])*)"
      | '((?:\\.|[^'\\])*)'
      | `((?:\\.|[^`\\])*)`
    )""",
    re.VERBOSE,
)
QUOTED_STRING_PATTERN = re.compile(
    r"""(?:"((?:\\.|[^"\\])*)"|'((?:\\.|[^'\\])*)'|`((?:\\.|[^`\\])*)`)"""
)
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class Finding:
    severity: str
    rule_id: str
    message: str
    path: str | None = None
    line: int | None = None
    evidence: str | None = None


class Context:
    def __init__(self) -> None:
        self.findings: list[Finding] = []
        self.scanned_files = 0

    def error(
        self,
        rule_id: str,
        message: str,
        *,
        path: Path | str | None = None,
        line: int | None = None,
        evidence: str | None = None,
    ) -> None:
        self.findings.append(
            Finding(
                "ERROR",
                rule_id,
                message,
                str(path) if path is not None else None,
                line,
                evidence,
            )
        )

    def warning(
        self,
        rule_id: str,
        message: str,
        *,
        path: Path | str | None = None,
        line: int | None = None,
        evidence: str | None = None,
    ) -> None:
        self.findings.append(
            Finding(
                "WARNING",
                rule_id,
                message,
                str(path) if path is not None else None,
                line,
                evidence,
            )
        )

    @property
    def errors(self) -> list[Finding]:
        return [x for x in self.findings if x.severity == "ERROR"]

    @property
    def warnings(self) -> list[Finding]:
        return [x for x in self.findings if x.severity == "WARNING"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate NDSP UI/UX Governance Supersession V2.",
    )
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--policy", type=Path, default=DEFAULT_V2_POLICY)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--changed-files",
        type=Path,
        help="Newline-delimited repository-relative paths to scan.",
    )
    parser.add_argument(
        "--full-source-scan",
        action="store_true",
        help="Scan every tracked-like source file under the repository.",
    )
    parser.add_argument("--policy-only", action="store_true")
    parser.add_argument("--strict-warnings", action="store_true")
    parser.add_argument("--no-write-report", action="store_true")
    return parser.parse_args()


def resolve(repo_root: Path, path: Path) -> Path:
    return path if path.is_absolute() else repo_root / path


def load_yaml(path: Path, context: Context) -> dict[str, Any]:
    if not path.is_file():
        context.error("V2_POLICY_MISSING", "V2 policy file is missing.", path=path)
        return {}
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        context.error(
            "V2_POLICY_PARSE_FAILED",
            f"Unable to parse V2 policy: {exc}",
            path=path,
        )
        return {}
    if not isinstance(value, dict):
        context.error(
            "V2_POLICY_ROOT_INVALID",
            "V2 policy root must be a mapping.",
            path=path,
        )
        return {}
    return value


def mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def sequence(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def exact_sequence(
    context: Context,
    actual: Any,
    expected: Iterable[str],
    *,
    rule_id: str,
    label: str,
) -> None:
    actual_list = [str(x) for x in sequence(actual)]
    expected_list = list(expected)
    if actual_list != expected_list:
        context.error(
            rule_id,
            f"{label} must exactly equal {expected_list!r}; got {actual_list!r}.",
        )


def validate_v2_policy(
    policy: Mapping[str, Any],
    context: Context,
) -> tuple[set[str], set[str], list[str]]:
    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        context.error(
            "V2_POLICY_ID_INVALID",
            f"policy_id must be {EXPECTED_POLICY_ID}.",
        )
    if policy.get("status") != "ACTIVE":
        context.error("V2_STATUS_INVALID", "V2 status must be ACTIVE.")
    if policy.get("enforcement") != "MANDATORY":
        context.error(
            "V2_ENFORCEMENT_INVALID",
            "V2 enforcement must be MANDATORY.",
        )
    if policy.get("owner_approval") != "EXPLICIT_OWNER_INSTRUCTION":
        context.error(
            "V2_OWNER_APPROVAL_MISSING",
            "V2 must retain explicit owner approval.",
        )

    precedence = mapping(policy.get("precedence"))
    if precedence.get("baseline_policy") != "UI_BACKEND_GOVERNANCE_POLICY.yaml":
        context.error(
            "V2_BASELINE_PRECEDENCE_INVALID",
            "V2 baseline policy reference is invalid.",
        )
    if precedence.get("merge_rule") != "MERGE_NOT_REWRITE":
        context.error(
            "V2_MERGE_RULE_INVALID",
            "V2 merge rule must remain MERGE_NOT_REWRITE.",
        )
    if precedence.get("unique_content_preserved") is not True:
        context.error(
            "V2_UNIQUE_CONTENT_NOT_PRESERVED",
            "V2 must preserve unique content.",
        )

    repo_safety = mapping(policy.get("repository_safety"))
    if repo_safety.get("full_confidential_master_report_in_public_repo") != "FORBIDDEN":
        context.error(
            "CONFIDENTIAL_MASTER_REPOSITORY_POLICY_INVALID",
            "Full confidential master report must remain forbidden in public repo.",
        )

    visual = mapping(policy.get("visual_identity"))
    for key, expected in EXPECTED_VISUAL_IDENTITY.items():
        if visual.get(key) != expected:
            context.error(
                "V2_VISUAL_IDENTITY_DRIFT",
                f"visual_identity.{key} must equal {expected!r}.",
            )
    if visual.get("indigo_violet_primary_brand_accent") is not False:
        context.error(
            "LEGACY_PRIMARY_BRAND_REINTRODUCED",
            "Indigo/Violet cannot be restored as the primary NDSP brand accent.",
        )
    if visual.get("motion") != "SUBTLE_ONLY":
        context.error(
            "V2_MOTION_POLICY_DRIFT",
            "V2 motion must remain SUBTLE_ONLY.",
        )
    if visual.get("reduced_motion_required") is not True:
        context.error(
            "V2_REDUCED_MOTION_DISABLED",
            "Reduced motion support must remain mandatory.",
        )

    invariants = mapping(policy.get("architecture_invariants"))
    for key, expected in EXPECTED_ARCHITECTURE_INVARIANTS.items():
        if invariants.get(key) != expected:
            context.error(
                "ARCHITECTURE_INVARIANT_DRIFT",
                f"architecture_invariants.{key} must equal {expected!r}.",
            )

    exposure = mapping(policy.get("customer_terminology_exposure"))
    if exposure.get("mode") != "NAME_ONLY":
        context.error(
            "CUSTOMER_EXPOSURE_MODE_INVALID",
            "Customer terminology exposure must remain NAME_ONLY.",
        )
    if exposure.get("maximum_approved_named_items") != 5:
        context.error(
            "CUSTOMER_VISIBLE_NAME_LIMIT_INVALID",
            "Maximum approved named items must remain exactly 5.",
        )
    exact_sequence(
        context,
        exposure.get("approved_customer_visible_names"),
        EXPECTED_APPROVED_NAMES,
        rule_id="CUSTOMER_VISIBLE_ALLOWLIST_DRIFT",
        label="approved_customer_visible_names",
    )
    if exposure.get("protected_internal_names_remaining") != 11:
        context.error(
            "PROTECTED_INTERNAL_NAME_COUNT_INVALID",
            "Exactly 11 internal names must remain protected.",
        )
    if exposure.get("protected_names_publicly_exposed") is not False:
        context.error(
            "PROTECTED_INTERNAL_NAMES_EXPOSED",
            "Protected internal names must never be publicly exposed.",
        )

    confidentiality = mapping(policy.get("confidentiality"))
    required_confidentiality = {
        "internal_existence_does_not_equal_public_authorization": True,
        "paid_entitlement_does_not_equal_ip_disclosure": True,
        "secret_data_sent_to_browser_then_hidden": "FORBIDDEN",
        "css_only_locking": "FORBIDDEN",
        "server_side_authorization_required": True,
        "server_side_entitlement_required": True,
    }
    for key, expected in required_confidentiality.items():
        if confidentiality.get(key) != expected:
            context.error(
                "CONFIDENTIALITY_GUARD_DRIFT",
                f"confidentiality.{key} must equal {expected!r}.",
            )
    forbidden_tokens = {
        str(x).strip()
        for x in sequence(confidentiality.get("forbidden_customer_disclosure"))
        if str(x).strip()
    }
    if len(forbidden_tokens) < 10:
        context.error(
            "CONFIDENTIALITY_FORBIDDEN_SET_TOO_SMALL",
            "Forbidden customer-disclosure set was unexpectedly reduced.",
        )

    public_exp = mapping(policy.get("public_experience"))
    if public_exp.get("internal_logic_exposure") is not False:
        context.error(
            "PUBLIC_INTERNAL_LOGIC_EXPOSURE_ENABLED",
            "Public internal-logic exposure must remain disabled.",
        )

    subscription = mapping(policy.get("subscription_architecture"))
    exact_sequence(
        context,
        subscription.get("customer_facing_plans"),
        EXPECTED_PLANS,
        rule_id="SUBSCRIPTION_PLAN_SET_DRIFT",
        label="customer_facing_plans",
    )
    if subscription.get("hard_code_unverified_prices_or_limits_in_ui") != "FORBIDDEN":
        context.error(
            "UNVERIFIED_COMMERCIAL_HARDCODE_ALLOWED",
            "Unverified prices/limits must remain forbidden in UI.",
        )
    if subscription.get("admin_rbac_separate_from_customer_subscription_entitlement") is not True:
        context.error(
            "RBAC_ENTITLEMENT_BOUNDARY_BROKEN",
            "Admin RBAC must remain separate from customer subscription entitlement.",
        )

    trial = mapping(policy.get("trial_and_entitlement"))
    if trial.get("trial_duration_days") != 16:
        context.error(
            "TRIAL_DURATION_DRIFT",
            "NDSP trial duration must remain 16 days.",
        )
    exact_sequence(
        context,
        trial.get("trial_visible_names"),
        EXPECTED_APPROVED_NAMES,
        rule_id="TRIAL_VISIBLE_ALLOWLIST_DRIFT",
        label="trial_visible_names",
    )
    if trial.get("post_trial_visibility") != "SERVER_SIDE_PLAN_ENTITLEMENT":
        context.error(
            "POST_TRIAL_ENTITLEMENT_NOT_SERVER_SIDE",
            "Post-trial visibility must remain server-side entitlement.",
        )
    matrix = mapping(trial.get("entitlement_matrix"))
    for plan, expected_names in EXPECTED_ENTITLEMENTS.items():
        plan_config = mapping(matrix.get(plan))
        exact_sequence(
            context,
            plan_config.get("visible_names"),
            expected_names,
            rule_id="ENTITLEMENT_MATRIX_DRIFT",
            label=f"entitlement_matrix.{plan}.visible_names",
        )

    locked = mapping(policy.get("locked_state_design"))
    for key in ("secret_name_rendered_then_blurred", "secret_name_rendered_then_masked"):
        if locked.get(key) != "FORBIDDEN":
            context.error(
                "LOCKED_SECRET_RENDERING_ALLOWED",
                f"locked_state_design.{key} must remain FORBIDDEN.",
            )
    generic_labels = {
        str(x).strip()
        for x in sequence(locked.get("approved_generic_labels"))
        if str(x).strip()
    }

    machine = mapping(policy.get("machine_enforcement"))
    expected_machine = {
        "validator_path": "scripts/governance/validate_uiux_governance_v2.py",
        "workflow_path": ".github/workflows/ui-backend-governance-policy.yml",
        "unit_test_path": "scripts/governance/tests/test_validate_uiux_governance_v2.py",
        "pull_request_changed_file_enforcement": True,
        "push_changed_file_enforcement": True,
        "full_repository_scan_available": True,
    }
    for key, expected in expected_machine.items():
        if machine.get(key) != expected:
            context.error(
                "V2_MACHINE_ENFORCEMENT_DRIFT",
                f"machine_enforcement.{key} must equal {expected!r}.",
            )
    required_ci_failures = {
        "v2_policy_drift",
        "legacy_primary_brand_reintroduced",
        "more_than_five_customer_visible_names",
        "unapproved_customer_visible_name",
        "confidential_field_in_customer_or_public_api",
        "confidential_master_committed_to_public_repo",
        "decision_layer_number_exposure",
    }
    actual_ci_failures = {
        str(x) for x in sequence(machine.get("ci_fail_on"))
    }
    missing_ci_failures = sorted(required_ci_failures - actual_ci_failures)
    if missing_ci_failures:
        context.error(
            "V2_MACHINE_CI_FAILURES_MISSING",
            "machine_enforcement.ci_fail_on is missing: "
            + ", ".join(missing_ci_failures),
        )

    artifacts = mapping(policy.get("canonical_private_artifacts"))
    private_filenames: list[str] = []
    for kind in ("markdown", "pdf", "docx"):
        item = mapping(artifacts.get(kind))
        filename = str(item.get("filename", "")).strip()
        digest = str(item.get("sha256", "")).strip()
        if not filename or PRIVATE_MASTER_SUFFIX not in filename:
            context.error(
                "PRIVATE_ARTIFACT_FILENAME_INVALID",
                f"canonical_private_artifacts.{kind}.filename is invalid.",
            )
        else:
            private_filenames.append(filename)
        if not SHA256_PATTERN.fullmatch(digest):
            context.error(
                "PRIVATE_ARTIFACT_HASH_INVALID",
                f"canonical_private_artifacts.{kind}.sha256 is invalid.",
            )

    return set(EXPECTED_APPROVED_NAMES), generic_labels, private_filenames


def normalized_path(path: Path) -> str:
    return "/" + path.as_posix().lower().strip("/") + "/"


def is_customer_source(path: Path) -> bool:
    norm = normalized_path(path)
    if any(marker in norm for marker in EXCLUDED_EXPOSURE_MARKERS):
        return False
    return any(marker in norm for marker in CUSTOMER_PATH_MARKERS)


def is_design_token_source(path: Path) -> bool:
    norm = normalized_path(path)
    if any(marker in norm for marker in EXCLUDED_EXPOSURE_MARKERS):
        return False
    return (
        is_customer_source(path)
        or any(marker in norm for marker in DESIGN_TOKEN_MARKERS)
        or path.name.lower() in {
            "tailwind.config.js",
            "tailwind.config.ts",
            "theme.ts",
            "theme.js",
            "tokens.ts",
            "tokens.js",
            "globals.css",
            "index.css",
        }
    )


def is_public_api_source(path: Path, content: str) -> bool:
    norm = normalized_path(path)
    if any(marker in norm for marker in EXCLUDED_EXPOSURE_MARKERS):
        return False
    if "/backend/" not in norm and "/apps/" not in norm:
        return False
    lowered = content.lower()
    return (
        "/public" in norm
        or "public" in path.name.lower()
        or any(marker in lowered for marker in PUBLIC_API_CONTENT_MARKERS)
    )


def snake_to_camel(value: str) -> str:
    head, *tail = value.split("_")
    return head + "".join(part[:1].upper() + part[1:] for part in tail)


def disclosure_token_variants(tokens: set[str]) -> set[str]:
    variants: set[str] = set()
    for token in tokens:
        cleaned = token.strip()
        if not cleaned:
            continue
        variants.add(cleaned)
        if "_" in cleaned:
            variants.add(snake_to_camel(cleaned))
    variants.update({"formula", "algorithm", "producer"})
    return variants


def build_sensitive_field_pattern(tokens: set[str]) -> re.Pattern[str]:
    variants = sorted(
        disclosure_token_variants(tokens),
        key=len,
        reverse=True,
    )
    alternation = "|".join(re.escape(v) for v in variants)
    return re.compile(
        rf"""(?ix)
        (?:
            ["'`]\s*(?:{alternation})\s*["'`]\s*:
          | \.\s*(?:{alternation})\b
          | \b(?:{alternation})\b\s*:
          | \b(?:{alternation})\b\s*=
        )
        """
    )


def find_line_number(content: str, index: int) -> int:
    return content.count("\n", 0, index) + 1


def scan_display_lists(
    path: Path,
    content: str,
    approved_names: set[str],
    generic_labels: set[str],
    context: Context,
) -> None:
    allowed = approved_names | generic_labels
    for match in DISPLAY_LIST_PATTERN.finditer(content):
        values = [
            next(part for part in groups if part is not None).strip()
            for groups in QUOTED_STRING_PATTERN.findall(match.group(1))
        ]
        if len(values) > 5:
            context.error(
                "CUSTOMER_VISIBLE_LIST_EXCEEDS_FIVE",
                "Customer-visible decision-intelligence name list exceeds five items.",
                path=path,
                line=find_line_number(content, match.start()),
                evidence=", ".join(values[:10]),
            )
        unapproved = [x for x in values if x not in allowed]
        if unapproved:
            context.error(
                "UNAPPROVED_CUSTOMER_VISIBLE_NAME",
                "Customer-facing name list contains a value outside the public-safe allowlist.",
                path=path,
                line=find_line_number(content, match.start()),
                evidence=", ".join(unapproved[:10]),
            )

    for match in DISPLAY_SINGLE_PATTERN.finditer(content):
        value = next(
            part for part in match.groups() if part is not None
        ).strip()
        if value not in allowed:
            context.error(
                "UNAPPROVED_CUSTOMER_VISIBLE_NAME",
                "Customer-facing decision layer name is outside the public-safe allowlist.",
                path=path,
                line=find_line_number(content, match.start()),
                evidence=value,
            )


def scan_source_file(
    relative_path: Path,
    full_path: Path,
    approved_names: set[str],
    generic_labels: set[str],
    forbidden_tokens: set[str],
    context: Context,
) -> None:
    if full_path.suffix.lower() not in SCANNABLE_SUFFIXES:
        return
    try:
        content = full_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        context.warning(
            "V2_SOURCE_READ_FAILED",
            f"Unable to read changed file: {exc}",
            path=relative_path,
        )
        return

    customer = is_customer_source(relative_path)
    public_api = is_public_api_source(relative_path, content)
    design_tokens = is_design_token_source(relative_path)
    if not (customer or public_api or design_tokens):
        return

    context.scanned_files += 1

    if design_tokens:
        for line_number, line in enumerate(content.splitlines(), start=1):
            if (
                OLD_PRIMARY_BRAND_PATTERN.search(line)
                and not OLD_PRIMARY_EXEMPT_PATTERN.search(line)
            ):
                context.error(
                    "LEGACY_PRIMARY_BRAND_COLOR_IN_CHANGED_UI",
                    "Changed UI/design token source appears to restore Indigo/Violet as primary/brand color.",
                    path=relative_path,
                    line=line_number,
                    evidence=line.strip()[:300],
                )

    if customer:
        numbered = DECISION_LAYER_NUMBER_PATTERN.search(content)
        if numbered:
            context.error(
                "CUSTOMER_DECISION_LAYER_NUMBER_EXPOSURE",
                "Customer-facing UI must not expose Decision Layers 01-16 as numbered internal structure.",
                path=relative_path,
                line=find_line_number(content, numbered.start()),
                evidence=numbered.group(0),
            )
        scan_display_lists(
            relative_path,
            content,
            approved_names,
            generic_labels,
            context,
        )

    if customer or public_api:
        sensitive_pattern = build_sensitive_field_pattern(forbidden_tokens)
        for match in sensitive_pattern.finditer(content):
            context.error(
                "CONFIDENTIAL_FIELD_IN_CUSTOMER_OR_PUBLIC_API",
                "Changed customer/public API source contains a forbidden proprietary field.",
                path=relative_path,
                line=find_line_number(content, match.start()),
                evidence=match.group(0)[:200],
            )


def read_changed_paths(
    repo_root: Path,
    changed_file_list: Path,
    context: Context,
) -> list[Path]:
    resolved = resolve(repo_root, changed_file_list)
    if not resolved.is_file():
        context.error(
            "CHANGED_FILE_LIST_MISSING",
            "Changed-file list does not exist.",
            path=resolved,
        )
        return []
    paths: list[Path] = []
    for raw in resolved.read_text(encoding="utf-8", errors="replace").splitlines():
        value = raw.strip()
        if not value:
            continue
        path = Path(value)
        if path.is_absolute() or ".." in path.parts:
            context.error(
                "CHANGED_FILE_PATH_INVALID",
                "Changed-file path must be repository-relative.",
                evidence=value,
            )
            continue
        paths.append(path)
    return paths


def iter_full_source_paths(repo_root: Path) -> Iterable[Path]:
    ignored = {".git", "node_modules", "dist", "build", "coverage", "__pycache__"}
    for full_path in repo_root.rglob("*"):
        if not full_path.is_file():
            continue
        relative = full_path.relative_to(repo_root)
        if any(part in ignored for part in relative.parts):
            continue
        yield relative


def enforce_private_artifact_absence(
    repo_root: Path,
    private_filenames: Iterable[str],
    context: Context,
) -> None:
    for filename in private_filenames:
        for match in repo_root.rglob(filename):
            if ".git" in match.parts:
                continue
            context.error(
                "CONFIDENTIAL_MASTER_COMMITTED_TO_PUBLIC_REPO",
                "A full confidential master artifact is present in the public repository.",
                path=match.relative_to(repo_root),
            )


def write_report(
    report_path: Path,
    *,
    policy_path: Path,
    context: Context,
    changed_file_list: Path | None,
    full_source_scan: bool,
    strict_warnings: bool,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "2.0",
        "validator": "validate_uiux_governance_v2.py",
        "policy_path": str(policy_path),
        "changed_file_list": str(changed_file_list) if changed_file_list else None,
        "full_source_scan": full_source_scan,
        "scanned_file_count": context.scanned_files,
        "error_count": len(context.errors),
        "warning_count": len(context.warnings),
        "strict_warnings": strict_warnings,
        "validation": (
            "PASS"
            if not context.errors
            and not (strict_warnings and context.warnings)
            else "FAIL"
        ),
        "findings": [asdict(x) for x in context.findings],
    }
    report_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def print_findings(context: Context) -> None:
    for item in context.findings:
        location = ""
        if item.path:
            location = f" location={item.path}"
            if item.line is not None:
                location += f":{item.line}"
        print(
            f"{item.severity.lower()}={item.rule_id}: "
            f"{item.message}{location}"
        )
        if item.evidence:
            print(f"evidence={item.evidence}")


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    policy_path = resolve(repo_root, args.policy).resolve()
    report_path = resolve(repo_root, args.report).resolve()
    context = Context()

    if not repo_root.is_dir():
        context.error(
            "REPOSITORY_ROOT_MISSING",
            "Repository root does not exist.",
            path=repo_root,
        )
        policy: dict[str, Any] = {}
        approved_names: set[str] = set()
        generic_labels: set[str] = set()
        private_filenames: list[str] = []
        forbidden_tokens: set[str] = set()
    else:
        policy = load_yaml(policy_path, context)
        approved_names, generic_labels, private_filenames = validate_v2_policy(
            policy,
            context,
        )
        confidentiality = mapping(policy.get("confidentiality"))
        forbidden_tokens = {
            str(x).strip()
            for x in sequence(confidentiality.get("forbidden_customer_disclosure"))
            if str(x).strip()
        }

        enforce_private_artifact_absence(
            repo_root,
            private_filenames,
            context,
        )

        if not args.policy_only:
            if args.changed_files and args.full_source_scan:
                context.error(
                    "SCAN_MODE_CONFLICT",
                    "Use either --changed-files or --full-source-scan, not both.",
                )
                source_paths: list[Path] = []
            elif args.changed_files:
                source_paths = read_changed_paths(
                    repo_root,
                    args.changed_files,
                    context,
                )
            elif args.full_source_scan:
                source_paths = list(iter_full_source_paths(repo_root))
            else:
                source_paths = []

            for relative_path in source_paths:
                full_path = repo_root / relative_path
                if not full_path.is_file():
                    # Deletions are intentionally ignored by content scanners.
                    continue
                scan_source_file(
                    relative_path,
                    full_path,
                    approved_names,
                    generic_labels,
                    forbidden_tokens,
                    context,
                )

    if not args.no_write_report:
        try:
            write_report(
                report_path,
                policy_path=policy_path,
                context=context,
                changed_file_list=args.changed_files,
                full_source_scan=args.full_source_scan,
                strict_warnings=args.strict_warnings,
            )
            print(f"report_path={report_path}")
        except OSError as exc:
            context.error(
                "REPORT_WRITE_FAILED",
                f"Unable to write V2 validation report: {exc}",
                path=report_path,
            )

    print_findings(context)
    failed = bool(context.errors) or (
        args.strict_warnings and bool(context.warnings)
    )
    print(f"policy_id={policy.get('policy_id', '')}")
    print(f"scanned_file_count={context.scanned_files}")
    print(f"error_count={len(context.errors)}")
    print(f"warning_count={len(context.warnings)}")
    if failed:
        print("validation=FAIL")
        print("status=UIUX_GOVERNANCE_V2_INVALID")
        return 1

    print("validation=PASS")
    print("status=UIUX_GOVERNANCE_V2_VALID")
    return 0


if __name__ == "__main__":
    sys.exit(main())
