"""
Governance v6 quarantine.

Legacy signal evaluation disabled.

Reason:
- NDSP is decision intelligence, not a signal engine.
- Direct signal performance evaluation is not part of the governed external decision-delivery path.
"""


def main():
    print({
        "status": "blocked",
        "reason": "legacy_signal_evaluator_disabled_by_governance_v6",
    })


if __name__ == "__main__":
    main()
