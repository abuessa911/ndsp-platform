#!/usr/bin/env python3
"""Validate the NDSP UI and backend governance policy.

The validator performs two levels of enforcement:

1. Policy validation:
   Ensures that the YAML policy contains all mandatory sections, approved
   technology choices, CORE/EXPANDED separation rules, accessibility rules,
   traceability requirements, and CI enforcement directives.

2. Repository validation:
   Scans package manifests and selected source files for clear violations such
   as unapproved duplicate UI libraries, public exposure of EXPANDED, missing
   TypeScript configuration in governed frontend applications, and direct
   presentation-layer fetch calls.

The script is read-only. It never mutates repository files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

try:
    import yaml
except ImportError as exc:
    print("error=Missing dependency: PyYAML")
    print("hint=python3 -m pip install PyYAML")
    print("validation=FAIL")
    print("status=UI_BACKEND_GOVERNANCE_POLICY_INVALID")
    raise SystemExit(1) from exc


DEFAULT_POLICY_PATH = Path(
    "docs/99-governance/ui-architecture/"
    "UI_BACKEND_GOVERNANCE_POLICY.yaml"
)
DEFAULT_REPORT_PATH = Path(
    "docs/99-governance/ui-architecture/"
    "UI_BACKEND_GOVERNANCE_VALIDATION_REPORT.json"
)

ALLOWED_STATUS = {"ACTIVE"}
ALLOWED_ENFORCEMENT = {"MANDATORY"}
ALLOWED_REAL_DATA_STATES = {"REAL_LIVE", "REAL_SNAPSHOT"}

REQUIRED_TOP_LEVEL_KEYS = {
    "schema_version",
    "policy_id",
    "title",
    "title_ar",
    "status",
    "enforcement",
    "effective_from",
    "owners",
    "purpose",
    "scope",
    "design_references",
    "architecture",
    "core_expanded_separation",
    "public_frontend",
    "admin_frontend",
    "settings",
    "sensitive_actions",
    "documentation_center",
    "visual_identity",
    "internationalization",
    "frontend_libraries",
    "library_admission_policy",
    "api_and_contracts",
    "traceability",
    "temporary_model_policy",
    "testing_and_quality",
    "security",
    "change_governance",
    "machine_enforcement",
}

REQUIRED_PUBLIC_ROUTES = {
    "Home",
    "Methodology",
    "Current Analysis",
    "Documentation",
    "Sign In",
}

REQUIRED_ADMIN_ROUTES = {
    "/admin/cot/overview",
    "/admin/cot/reports",
    "/admin/cot/daily-control",
    "/admin/cot/experiments",
    "/admin/cot/comparisons",
    "/admin/cot/governance",
    "/admin/cot/audit-logs",
    "/admin/cot/contracts",
    "/admin/cot/settings",
}

REQUIRED_TRACEABILITY_FIELDS = {
    "screen",
    "function",
    "capability",
    "service",
    "endpoint",
    "data_source",
    "component",
    "permission",
    "test",
}

REQUIRED_UI_COMPLETE_RULES = {
    "screen_defined",
    "visible_component_defined",
    "service_defined",
    "endpoint_or_contract_defined",
    "real_data_defined",
    "permission_defined",
    "loading_state_defined",
    "empty_state_defined",
    "error_state_defined",
    "success_state_defined",
    "executable_test_defined",
}

REQUIRED_FRONTEND_LIBRARIES = {
    "shadcn/ui",
    "Radix UI",
    "Lucide React",
    "React Hook Form",
    "Zod",
    "TanStack Query",
    "AG Grid",
    "Recharts",
    "Apache ECharts",
    "React Flow",
    "Leaflet",
    "TipTap",
    "Monaco Editor",
    "FullCalendar",
    "dnd-kit",
    "Vitest",
    "Testing Library",
    "Playwright",
    "Storybook",
    "MSW",
    "date-fns",
}

PACKAGE_TO_POLICY_NAME = {
    "@radix-ui": "Radix UI",
    "lucide-react": "Lucide React",
    "react-hook-form": "React Hook Form",
    "zod": "Zod",
    "@tanstack/react-query": "TanStack Query",
    "@tanstack/react-router": "TanStack Router",
    "react-router": "React Router",
    "react-router-dom": "React Router",
    "ag-grid-community": "AG Grid",
    "ag-grid-react": "AG Grid",
    "ag-grid-enterprise": "AG Grid",
    "recharts": "Recharts",
    "echarts": "Apache ECharts",
    "echarts-for-react": "Apache ECharts",
    "@xyflow/react": "React Flow",
    "reactflow": "React Flow",
    "leaflet": "Leaflet",
    "react-leaflet": "Leaflet",
    "mapbox-gl": "Mapbox GL",
    "maplibre-gl": "MapLibre GL",
    "@tiptap": "TipTap",
    "monaco-editor": "Monaco Editor",
    "@monaco-editor/react": "Monaco Editor",
    "@fullcalendar": "FullCalendar",
    "@dnd-kit": "dnd-kit",
    "@react-three/fiber": "React Three Fiber",
    "three": "React Three Fiber",
    "date-fns": "date-fns",
    "i18next": "i18next",
    "react-i18next": "i18next",
    "react-intl": "react-intl",
    "vitest": "Vitest",
    "@testing-library": "Testing Library",
    "@playwright/test": "Playwright",
    "msw": "MSW",
    "storybook": "Storybook",
    "@storybook": "Storybook",
}

DISALLOWED_DUPLICATE_UI_PACKAGES = {
    "@mui/material": "Unapproved duplicate base UI library",
    "antd": "Unapproved duplicate base UI library",
    "@chakra-ui/react": "Unapproved duplicate base UI library",
    "semantic-ui-react": "Unapproved duplicate base UI library",
    "bootstrap": "Unapproved duplicate base UI library",
    "react-bootstrap": "Unapproved duplicate base UI library",
}

SOURCE_SUFFIXES = {
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".py",
    ".json",
    ".yaml",
    ".yml",
}

IGNORED_DIRS = {
    ".git",
    ".next",
    ".turbo",
    ".vite",
    "coverage",
    "dist",
    "build",
    "node_modules",
    "vendor",
    "_backups",
    "__pycache__",
}

PUBLIC_PATH_MARKERS = {
    "/public/",
    "/pages/",
    "/routes/public/",
    "/components/public/",
    "/src/public/",
    "/src/pages/",
}

DIRECT_FETCH_PATTERN = re.compile(r"\bfetch\s*\(")
EXPANDED_PATTERN = re.compile(r"\bEXPANDED\b|\bSHADOW_MODE\b", re.IGNORECASE)
PUBLIC_API_PATTERN = re.compile(
    r"public[_\-\s]?api|/api/public|public result", re.IGNORECASE
)
ALLOW_COMMENT_PATTERN = re.compile(
    r"governance-allow:\s*(expanded-public-reference|direct-fetch)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Finding:
    severity: str
    rule_id: str
    message: str
    path: str | None = None
    line: int | None = None
    evidence: str | None = None


class ValidationContext:
    """Collects deterministic validation findings."""

    def __init__(self) -> None:
        self.findings: list[Finding] = []

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
                severity="ERROR",
                rule_id=rule_id,
                message=message,
                path=str(path) if path is not None else None,
                line=line,
                evidence=evidence,
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
                severity="WARNING",
                rule_id=rule_id,
                message=message,
                path=str(path) if path is not None else None,
                line=line,
                evidence=evidence,
            )
        )

    @property
    def errors(self) -> list[Finding]:
        return [item for item in self.findings if item.severity == "ERROR"]

    @property
    def warnings(self) -> list[Finding]:
        return [item for item in self.findings if item.severity == "WARNING"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate NDSP UI/backend governance policy.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--policy",
        type=Path,
        default=DEFAULT_POLICY_PATH,
        help="Policy path relative to repo root unless absolute.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT_PATH,
        help="JSON report path relative to repo root unless absolute.",
    )
    parser.add_argument(
        "--policy-only",
        action="store_true",
        help="Validate policy structure without scanning repository source.",
    )
    parser.add_argument(
        "--strict-warnings",
        action="store_true",
        help="Treat warnings as errors.",
    )
    parser.add_argument(
        "--no-write-report",
        action="store_true",
        help="Do not write the JSON validation report.",
    )
    return parser.parse_args()


def resolve_path(repo_root: Path, path: Path) -> Path:
    return path if path.is_absolute() else repo_root / path


def load_policy(path: Path, context: ValidationContext) -> dict[str, Any]:
    if not path.is_file():
        context.error(
            "POLICY_FILE_MISSING",
            "Governance policy file does not exist.",
            path=path,
        )
        return {}

    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        context.error(
            "POLICY_PARSE_FAILED",
            f"Unable to parse governance policy: {exc}",
            path=path,
        )
        return {}

    if not isinstance(payload, dict):
        context.error(
            "POLICY_ROOT_INVALID",
            "Policy root must be a YAML mapping.",
            path=path,
        )
        return {}

    return payload


def require_mapping(
    value: Any,
    path: str,
    context: ValidationContext,
) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        context.error(
            "TYPE_MAPPING_REQUIRED",
            f"{path} must be a mapping.",
        )
        return {}
    return value


def require_sequence(
    value: Any,
    path: str,
    context: ValidationContext,
) -> Sequence[Any]:
    if not isinstance(value, list):
        context.error(
            "TYPE_SEQUENCE_REQUIRED",
            f"{path} must be a list.",
        )
        return []
    return value


def require_non_empty_string(
    value: Any,
    path: str,
    context: ValidationContext,
) -> str:
    if not isinstance(value, str) or not value.strip():
        context.error(
            "NON_EMPTY_STRING_REQUIRED",
            f"{path} must be a non-empty string.",
        )
        return ""
    return value.strip()


def require_set_contains(
    actual: Iterable[Any],
    required: set[str],
    path: str,
    context: ValidationContext,
) -> None:
    normalized = {str(item) for item in actual}
    missing = sorted(required - normalized)
    if missing:
        context.error(
            "REQUIRED_VALUES_MISSING",
            f"{path} is missing required values: {', '.join(missing)}",
        )


def flatten_approved_libraries(frontend_libraries: Mapping[str, Any]) -> set[str]:
    approved: set[str] = set()

    library_list_keys = {
        "approved",
        "unit",
        "components",
        "end_to_end",
        "api_mocking",
        "component_documentation",
    }

    def visit(value: Any, parent_key: str | None = None) -> None:
        if isinstance(value, Mapping):
            for key, nested in value.items():
                if key in library_list_keys and isinstance(nested, list):
                    approved.update(str(item) for item in nested)
                else:
                    visit(nested, key)
        elif isinstance(value, list) and parent_key in library_list_keys:
            approved.update(str(item) for item in value)

    visit(frontend_libraries)
    return approved


def validate_policy_structure(
    policy: Mapping[str, Any],
    context: ValidationContext,
) -> set[str]:
    missing_top_level = sorted(REQUIRED_TOP_LEVEL_KEYS - set(policy))
    if missing_top_level:
        context.error(
            "TOP_LEVEL_SECTIONS_MISSING",
            "Missing top-level policy sections: "
            + ", ".join(missing_top_level),
        )

    if policy.get("status") not in ALLOWED_STATUS:
        context.error(
            "POLICY_STATUS_INVALID",
            f"status must be one of {sorted(ALLOWED_STATUS)}.",
        )

    if policy.get("enforcement") not in ALLOWED_ENFORCEMENT:
        context.error(
            "POLICY_ENFORCEMENT_INVALID",
            f"enforcement must be one of {sorted(ALLOWED_ENFORCEMENT)}.",
        )

    require_non_empty_string(
        policy.get("schema_version"),
        "schema_version",
        context,
    )
    require_non_empty_string(policy.get("policy_id"), "policy_id", context)
    require_non_empty_string(policy.get("title"), "title", context)
    require_non_empty_string(policy.get("title_ar"), "title_ar", context)

    owners = require_sequence(policy.get("owners"), "owners", context)
    if len(owners) < 2:
        context.error(
            "OWNERS_INSUFFICIENT",
            "Policy must define at least two responsible owners.",
        )

    architecture = require_mapping(
        policy.get("architecture"),
        "architecture",
        context,
    )
    frontend = require_mapping(
        architecture.get("frontend"),
        "architecture.frontend",
        context,
    )
    expected_frontend = {
        "framework": "React",
        "build_tool": "Vite",
        "language": "TypeScript",
    }
    for key, expected in expected_frontend.items():
        if frontend.get(key) != expected:
            context.error(
                "FRONTEND_STACK_INVALID",
                f"architecture.frontend.{key} must equal {expected!r}.",
            )

    governance_backend = require_mapping(
        architecture.get("governance_backend"),
        "architecture.governance_backend",
        context,
    )
    expected_backend = {
        "runtime": "Node.js",
        "framework": "Express",
        "module_system": "CommonJS",
        "contract_format": "JSON Schema",
    }
    for key, expected in expected_backend.items():
        if governance_backend.get(key) != expected:
            context.error(
                "BACKEND_STACK_INVALID",
                f"architecture.governance_backend.{key} "
                f"must equal {expected!r}.",
            )

    raw_gateway = require_mapping(
        architecture.get("raw_cot_gateway"),
        "architecture.raw_cot_gateway",
        context,
    )
    if raw_gateway.get("runtime") != "Python":
        context.error(
            "RAW_GATEWAY_RUNTIME_INVALID",
            "Raw COT gateway runtime must be Python.",
        )
    if raw_gateway.get("server") != "Uvicorn":
        context.error(
            "RAW_GATEWAY_SERVER_INVALID",
            "Raw COT gateway server must be Uvicorn.",
        )

    separation = require_mapping(
        policy.get("core_expanded_separation"),
        "core_expanded_separation",
        context,
    )
    if separation.get("mandatory") is not True:
        context.error(
            "CORE_EXPANDED_SEPARATION_NOT_MANDATORY",
            "CORE/EXPANDED separation must be mandatory.",
        )

    prohibited_flows = require_sequence(
        separation.get("prohibited_flows"),
        "core_expanded_separation.prohibited_flows",
        context,
    )
    required_prohibited_flows = {
        "EXPANDED Shadow Engine -> Public API",
        "Experimental Result Store -> Public API",
    }
    require_set_contains(
        prohibited_flows,
        required_prohibited_flows,
        "core_expanded_separation.prohibited_flows",
        context,
    )

    promotion = require_mapping(
        separation.get("promotion"),
        "core_expanded_separation.promotion",
        context,
    )
    if promotion.get("direct_promotion_allowed") is not False:
        context.error(
            "DIRECT_PROMOTION_ALLOWED",
            "Direct EXPANDED-to-CORE promotion must remain disabled.",
        )

    public_frontend = require_mapping(
        policy.get("public_frontend"),
        "public_frontend",
        context,
    )
    if public_frontend.get("visible_model") != "CORE":
        context.error(
            "PUBLIC_MODEL_INVALID",
            "Public frontend visible_model must be CORE.",
        )
    hidden_models = require_sequence(
        public_frontend.get("hidden_models"),
        "public_frontend.hidden_models",
        context,
    )
    require_set_contains(
        hidden_models,
        {"EXPANDED"},
        "public_frontend.hidden_models",
        context,
    )
    required_sections = require_sequence(
        public_frontend.get("required_sections"),
        "public_frontend.required_sections",
        context,
    )
    require_set_contains(
        required_sections,
        REQUIRED_PUBLIC_ROUTES,
        "public_frontend.required_sections",
        context,
    )

    admin_frontend = require_mapping(
        policy.get("admin_frontend"),
        "admin_frontend",
        context,
    )
    if admin_frontend.get("base_route") != "/admin/cot":
        context.error(
            "ADMIN_BASE_ROUTE_INVALID",
            "Admin base route must be /admin/cot.",
        )
    admin_routes = require_sequence(
        admin_frontend.get("required_routes"),
        "admin_frontend.required_routes",
        context,
    )
    require_set_contains(
        admin_routes,
        REQUIRED_ADMIN_ROUTES,
        "admin_frontend.required_routes",
        context,
    )

    internationalization = require_mapping(
        policy.get("internationalization"),
        "internationalization",
        context,
    )
    supported_languages = require_sequence(
        internationalization.get("supported_languages"),
        "internationalization.supported_languages",
        context,
    )
    require_set_contains(
        supported_languages,
        {"ar", "en"},
        "internationalization.supported_languages",
        context,
    )
    if internationalization.get("component_level_direction_required") is not True:
        context.error(
            "COMPONENT_DIRECTION_NOT_REQUIRED",
            "Component-level RTL/LTR direction must be required.",
        )

    traceability = require_mapping(
        policy.get("traceability"),
        "traceability",
        context,
    )
    if traceability.get("mandatory") is not True:
        context.error(
            "TRACEABILITY_NOT_MANDATORY",
            "UI traceability must be mandatory.",
        )
    traceability_mapping = require_sequence(
        traceability.get("mapping"),
        "traceability.mapping",
        context,
    )
    require_set_contains(
        traceability_mapping,
        REQUIRED_TRACEABILITY_FIELDS,
        "traceability.mapping",
        context,
    )
    ui_complete_rule = require_mapping(
        traceability.get("ui_complete_rule"),
        "traceability.ui_complete_rule",
        context,
    )
    all_required = require_sequence(
        ui_complete_rule.get("all_required"),
        "traceability.ui_complete_rule.all_required",
        context,
    )
    require_set_contains(
        all_required,
        REQUIRED_UI_COMPLETE_RULES,
        "traceability.ui_complete_rule.all_required",
        context,
    )

    testing = require_mapping(
        policy.get("testing_and_quality"),
        "testing_and_quality",
        context,
    )
    ci_failures = require_sequence(
        testing.get("ci_must_fail_on"),
        "testing_and_quality.ci_must_fail_on",
        context,
    )
    require_set_contains(
        ci_failures,
        {
            "public_exposure_of_expanded",
            "missing_required_contract",
            "ui_complete_without_required_evidence",
            "unapproved_library",
            "license_violation",
        },
        "testing_and_quality.ci_must_fail_on",
        context,
    )

    frontend_libraries = require_mapping(
        policy.get("frontend_libraries"),
        "frontend_libraries",
        context,
    )
    approved_libraries = flatten_approved_libraries(frontend_libraries)
    missing_libraries = sorted(
        REQUIRED_FRONTEND_LIBRARIES - approved_libraries
    )
    if missing_libraries:
        context.error(
            "APPROVED_LIBRARIES_MISSING",
            "Policy is missing approved libraries: "
            + ", ".join(missing_libraries),
        )

    machine = require_mapping(
        policy.get("machine_enforcement"),
        "machine_enforcement",
        context,
    )
    if machine.get("recommended_validator_path") != (
        "scripts/governance/validate_ui_backend_governance_policy.py"
    ):
        context.error(
            "VALIDATOR_PATH_INVALID",
            "machine_enforcement.recommended_validator_path is invalid.",
        )
    if machine.get("recommended_ci_path") != (
        ".github/workflows/ui-backend-governance-policy.yml"
    ):
        context.error(
            "WORKFLOW_PATH_INVALID",
            "machine_enforcement.recommended_ci_path is invalid.",
        )

    return approved_libraries


def iter_package_manifests(repo_root: Path) -> Iterable[Path]:
    for path in repo_root.rglob("package.json"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        yield path


def load_json_file(path: Path, context: ValidationContext) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        context.error(
            "JSON_PARSE_FAILED",
            f"Unable to parse JSON file: {exc}",
            path=path,
        )
        return {}

    if not isinstance(payload, dict):
        context.error(
            "JSON_ROOT_INVALID",
            "JSON root must be an object.",
            path=path,
        )
        return {}

    return payload


def collect_dependencies(manifest: Mapping[str, Any]) -> dict[str, str]:
    dependencies: dict[str, str] = {}
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        value = manifest.get(key)
        if isinstance(value, Mapping):
            dependencies.update(
                {
                    str(package): str(version)
                    for package, version in value.items()
                }
            )
    return dependencies


def policy_name_for_package(package: str) -> str | None:
    for prefix, policy_name in PACKAGE_TO_POLICY_NAME.items():
        if package == prefix or package.startswith(prefix + "/"):
            return policy_name
    return None


def looks_like_frontend_manifest(
    path: Path,
    manifest: Mapping[str, Any],
) -> bool:
    dependencies = collect_dependencies(manifest)
    return (
        "react" in dependencies
        or "vite" in dependencies
        or any(
            marker in path.as_posix().lower()
            for marker in ("frontend", "web", "ui", "dashboard")
        )
    )


def validate_package_manifests(
    repo_root: Path,
    approved_libraries: set[str],
    context: ValidationContext,
) -> None:
    manifests = list(iter_package_manifests(repo_root))
    if not manifests:
        context.warning(
            "NO_PACKAGE_MANIFESTS",
            "No package.json files were found for repository enforcement.",
        )
        return

    for manifest_path in manifests:
        manifest = load_json_file(manifest_path, context)
        if not manifest:
            continue

        dependencies = collect_dependencies(manifest)
        is_frontend = looks_like_frontend_manifest(manifest_path, manifest)

        if is_frontend:
            if "react" not in dependencies:
                context.warning(
                    "FRONTEND_REACT_MISSING",
                    "Frontend-like package does not declare React.",
                    path=manifest_path,
                )
            if "vite" not in dependencies:
                context.warning(
                    "FRONTEND_VITE_MISSING",
                    "Frontend-like package does not declare Vite.",
                    path=manifest_path,
                )

            tsconfig_candidates = [
                manifest_path.parent / "tsconfig.json",
                manifest_path.parent / "tsconfig.app.json",
            ]
            if not any(path.is_file() for path in tsconfig_candidates):
                context.warning(
                    "FRONTEND_TYPESCRIPT_CONFIG_MISSING",
                    "Frontend-like package has no tsconfig.json or "
                    "tsconfig.app.json.",
                    path=manifest_path.parent,
                )

        for package in sorted(dependencies):
            if package in DISALLOWED_DUPLICATE_UI_PACKAGES:
                context.error(
                    "UNAPPROVED_UI_LIBRARY",
                    DISALLOWED_DUPLICATE_UI_PACKAGES[package],
                    path=manifest_path,
                    evidence=package,
                )

            policy_name = policy_name_for_package(package)
            if policy_name and policy_name not in approved_libraries:
                context.error(
                    "LIBRARY_NOT_APPROVED_BY_POLICY",
                    f"{package} maps to {policy_name}, which is not approved.",
                    path=manifest_path,
                    evidence=package,
                )


def iter_source_files(repo_root: Path) -> Iterable[Path]:
    for path in repo_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SOURCE_SUFFIXES:
            continue
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        yield path


def is_public_source_path(path: Path) -> bool:
    normalized = "/" + path.as_posix().lower().strip("/") + "/"
    return any(marker in normalized for marker in PUBLIC_PATH_MARKERS)


def line_allows_exception(line: str, rule: str) -> bool:
    match = ALLOW_COMMENT_PATTERN.search(line)
    return bool(match and match.group(1).lower() == rule.lower())


def validate_source_files(
    repo_root: Path,
    context: ValidationContext,
) -> None:
    for source_path in iter_source_files(repo_root):
        relative_path = source_path.relative_to(repo_root)
        try:
            content = source_path.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except OSError as exc:
            context.warning(
                "SOURCE_READ_FAILED",
                f"Unable to read source file: {exc}",
                path=relative_path,
            )
            continue

        lines = content.splitlines()

        if is_public_source_path(relative_path):
            for line_number, line in enumerate(lines, start=1):
                if (
                    EXPANDED_PATTERN.search(line)
                    and PUBLIC_API_PATTERN.search(line)
                    and not line_allows_exception(
                        line,
                        "expanded-public-reference",
                    )
                ):
                    context.error(
                        "PUBLIC_EXPANDED_EXPOSURE",
                        "Public source appears to connect EXPANDED/SHADOW "
                        "content to a public API.",
                        path=relative_path,
                        line=line_number,
                        evidence=line.strip()[:300],
                    )

        normalized = "/" + relative_path.as_posix().lower().strip("/") + "/"
        is_presentation_component = (
            "/components/" in normalized
            or "/pages/" in normalized
            or "/views/" in normalized
        )

        if is_presentation_component and source_path.suffix.lower() in {
            ".jsx",
            ".tsx",
        }:
            for line_number, line in enumerate(lines, start=1):
                if (
                    DIRECT_FETCH_PATTERN.search(line)
                    and not line_allows_exception(line, "direct-fetch")
                ):
                    context.warning(
                        "DIRECT_FETCH_IN_PRESENTATION",
                        "Direct fetch() call found in a presentation component. "
                        "Use an API client and TanStack Query hook, or document "
                        "an exception.",
                        path=relative_path,
                        line=line_number,
                        evidence=line.strip()[:300],
                    )


def validate_required_project_paths(
    repo_root: Path,
    context: ValidationContext,
) -> None:
    recommended = {
        "governance backend": Path(
            "backend/services/decision_governance_core"
        ),
        "raw COT gateway": Path("apps/ndsp-raw-cot-gateway"),
    }

    for label, relative_path in recommended.items():
        if not (repo_root / relative_path).exists():
            context.warning(
                "RECOMMENDED_PATH_MISSING",
                f"Recommended {label} path does not exist.",
                path=relative_path,
            )


def write_report(
    report_path: Path,
    *,
    policy_path: Path,
    repo_root: Path,
    context: ValidationContext,
    policy_only: bool,
    strict_warnings: bool,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "1.0",
        "validator": "validate_ui_backend_governance_policy.py",
        "policy_path": str(policy_path),
        "repo_root": str(repo_root),
        "policy_only": policy_only,
        "strict_warnings": strict_warnings,
        "error_count": len(context.errors),
        "warning_count": len(context.warnings),
        "validation": (
            "PASS"
            if not context.errors
            and not (strict_warnings and context.warnings)
            else "FAIL"
        ),
        "findings": [asdict(item) for item in context.findings],
    }
    report_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def print_findings(context: ValidationContext) -> None:
    for finding in context.findings:
        location = ""
        if finding.path:
            location = finding.path
            if finding.line is not None:
                location += f":{finding.line}"
            location = f" location={location}"

        print(
            f"{finding.severity.lower()}={finding.rule_id}: "
            f"{finding.message}{location}"
        )
        if finding.evidence:
            print(f"evidence={finding.evidence}")


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    policy_path = resolve_path(repo_root, args.policy).resolve()
    report_path = resolve_path(repo_root, args.report).resolve()

    context = ValidationContext()

    if not repo_root.is_dir():
        context.error(
            "REPOSITORY_ROOT_MISSING",
            "Repository root does not exist.",
            path=repo_root,
        )
        policy: dict[str, Any] = {}
        approved_libraries: set[str] = set()
    else:
        policy = load_policy(policy_path, context)
        approved_libraries = validate_policy_structure(policy, context)

        if not args.policy_only:
            validate_package_manifests(
                repo_root,
                approved_libraries,
                context,
            )
            validate_source_files(repo_root, context)
            validate_required_project_paths(repo_root, context)

    if not args.no_write_report:
        try:
            write_report(
                report_path,
                policy_path=policy_path,
                repo_root=repo_root,
                context=context,
                policy_only=args.policy_only,
                strict_warnings=args.strict_warnings,
            )
            print(f"report_path={report_path}")
        except OSError as exc:
            context.error(
                "REPORT_WRITE_FAILED",
                f"Unable to write validation report: {exc}",
                path=report_path,
            )

    print_findings(context)

    failed = bool(context.errors) or (
        args.strict_warnings and bool(context.warnings)
    )

    print(f"policy_id={policy.get('policy_id', '')}")
    print(f"policy_status={policy.get('status', '')}")
    print(f"error_count={len(context.errors)}")
    print(f"warning_count={len(context.warnings)}")
    print(f"strict_warnings={str(args.strict_warnings).lower()}")
    print(f"policy_only={str(args.policy_only).lower()}")

    if failed:
        print("validation=FAIL")
        print("status=UI_BACKEND_GOVERNANCE_POLICY_INVALID")
        return 1

    print("validation=PASS")
    print("status=UI_BACKEND_GOVERNANCE_POLICY_VALID")
    return 0


if __name__ == "__main__":
    sys.exit(main())
