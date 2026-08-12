from __future__ import annotations

def check_entitlement(*, plan, feature, active=True, trial_days_remaining=None):
    allowed=bool(active and (plan in {"trial","premium","enterprise","owner"}))
    if plan=="trial" and (trial_days_remaining is None or trial_days_remaining<0):
        allowed=False
    return {
        "allowed":allowed,
        "plan":plan,
        "feature":feature,
        "controls_access_only":True,
        "changes_decision":False,
    }
