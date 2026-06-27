from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

MAX_BETA_USERS = 50


def _has_attr(model, name: str) -> bool:
    return hasattr(model, name)


def count_elite_trial_users(db: Session, UserModel) -> int:
    """
    Count Elite Trial users only.
    """

    q = db.query(UserModel)

    filters = []

    if _has_attr(UserModel, "plan"):
        filters.append(func.lower(getattr(UserModel, "plan")) == "elite")

    if _has_attr(UserModel, "current_plan"):
        filters.append(func.lower(getattr(UserModel, "current_plan")) == "elite")

    if _has_attr(UserModel, "package"):
        filters.append(func.lower(getattr(UserModel, "package")) == "elite")

    if filters:
        from sqlalchemy import or_
        q = q.filter(or_(*filters))

    return int(q.count())


def enforce_elite_trial_capacity(
    db: Session,
    UserModel,
    max_users: int = MAX_BETA_USERS,
) -> int:
    """
    Enforce Elite Trial capacity limit.
    """

    current_user_count = count_elite_trial_users(db, UserModel)

    if current_user_count >= max_users:
        raise HTTPException(
            status_code=403,
            detail=f"نعتذر، تم اكتمال الحد الأقصى للمشتركين في فترة تجربة النخبة ({max_users}/{max_users})."
        )

    return current_user_count
