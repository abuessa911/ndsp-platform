#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from test_ndsp_v4_1_stage_contract_safe import (
    publish_decision_contract,
    run_all_stage_tests,
    run_ndsp_v4_pipeline,
)


def main() -> int:
    mode = os.environ.get("NDSP_STAGE_TEST_MODE", "test").strip().lower()

    if mode == "single":
        contract = run_ndsp_v4_pipeline(
            "EURUSD",
            {"volatility_spike": True, "low_liquidity": True},
        )
        print(json.dumps(contract, ensure_ascii=False, indent=2, sort_keys=True))

        publish_result = publish_decision_contract(
            contract,
            stream_name=os.environ.get("REDIS_STREAM_NAME", "ndsp.decision.stream"),
            host=os.environ.get("REDIS_HOST", "127.0.0.1"),
            port=int(os.environ.get("REDIS_PORT", "6379")),
            db=int(os.environ.get("REDIS_DB", "0")),
            dry_run=os.environ.get("NDSP_REDIS_DRY_RUN", "1") != "0",
        )
        print(json.dumps(publish_result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    result = run_all_stage_tests()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
