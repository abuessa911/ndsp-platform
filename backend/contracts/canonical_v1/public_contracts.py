"""Canonical governed contracts for NDSP Public API V1.

This module owns public route metadata and explicit response allowlists.
Internal decision-layer structures must never be added to these contracts.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Final


PUBLIC_CONTRACT_VERSION: Final = "v1"

PUBLIC_ROUTE_CONTRACTS: Final[dict[str, dict[str, Any]]] = {
    "/api/public/overview": {
        "method": "GET",
        "version": PUBLIC_CONTRACT_VERSION,
        "access_policy": "public-read",
        "entitlement_required": False,
        "fields": {
            "mode": None,
            "updatedAt": None,
            "kpis": {
                "[]": {
                    "id": None,
                    "label": None,
                    "value": None,
                    "detail": None,
                    "status": None,
                }
            },
            "trend": {
                "[]": {
                    "label": None,
                    "value": None,
                }
            },
        },
    },
    "/api/public/core": {
        "method": "GET",
        "version": PUBLIC_CONTRACT_VERSION,
        "access_policy": "public-read",
        "entitlement_required": False,
        "fields": {
            "mode": None,
            "updatedAt": None,
            "direction": None,
            "summary": None,
            "governanceStatus": None,
            "evidenceStatus": None,
            "freshnessStatus": None,
        },
    },
    "/api/public/market-context": {
        "method": "GET",
        "version": PUBLIC_CONTRACT_VERSION,
        "access_policy": "public-read",
        "entitlement_required": False,
        "fields": {
            "mode": None,
            "updatedAt": None,
            "title": None,
            "summary": None,
            "contextSeries": {
                "[]": {
                    "label": None,
                    "value": None,
                }
            },
        },
    },
    "/api/public/evidence": {
        "method": "GET",
        "version": PUBLIC_CONTRACT_VERSION,
        "access_policy": "public-read",
        "entitlement_required": False,
        "fields": {
            "mode": None,
            "updatedAt": None,
            "rows": {
                "[]": {
                    "id": None,
                    "source": None,
                    "category": None,
                    "status": None,
                    "freshness": None,
                    "updatedAt": None,
                }
            },
        },
    },
}


def get_public_contract(path: str) -> dict[str, Any]:
    """Return a defensive copy of one registered public contract."""

    contract = PUBLIC_ROUTE_CONTRACTS.get(path)
    if contract is None:
        raise KeyError(f"public contract not registered: {path}")
    return deepcopy(contract)


def project_allowlisted(
    value: Any,
    specification: dict[str, Any] | None,
) -> Any:
    """Project a value through an explicit recursive allowlist."""

    if specification is None:
        return value

    if "[]" in specification:
        if not isinstance(value, list):
            return []
        item_specification = specification["[]"]
        return [
            project_allowlisted(item, item_specification)
            for item in value
            if isinstance(item, dict)
        ]

    if not isinstance(value, dict):
        return {}

    projected: dict[str, Any] = {}
    for key, child_specification in specification.items():
        if key not in value:
            continue
        projected[key] = project_allowlisted(
            value[key],
            child_specification,
        )

    return projected


def project_public_response(
    path: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Remove every field not explicitly authorized by the route contract."""

    contract = get_public_contract(path)
    return project_allowlisted(payload, contract["fields"])


def public_contract_manifest() -> dict[str, dict[str, Any]]:
    """Return non-sensitive metadata for registered public routes."""

    return {
        path: {
            "method": contract["method"],
            "version": contract["version"],
            "access_policy": contract["access_policy"],
            "entitlement_required": contract["entitlement_required"],
        }
        for path, contract in PUBLIC_ROUTE_CONTRACTS.items()
    }
