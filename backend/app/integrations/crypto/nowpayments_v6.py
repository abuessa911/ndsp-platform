from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


class NOWPaymentsError(RuntimeError):
    pass


def api_base() -> str:
    return os.getenv("NOWPAYMENTS_API_BASE", "https://api.nowpayments.io/v1").rstrip("/")


def api_key() -> str:
    key = os.getenv("NOWPAYMENTS_API_KEY", "")
    if not key:
        raise NOWPaymentsError("NOWPAYMENTS_API_KEY is missing")
    return key


def default_pay_currency() -> str:
    return os.getenv("NOWPAYMENTS_PAY_CURRENCY", "usdttrc20")


def default_price_currency() -> str:
    return os.getenv("NOWPAYMENTS_PRICE_CURRENCY", "usd")


def create_payment(
    *,
    price_amount: str,
    order_id: str,
    order_description: str,
    telegram_id: str,
    plan: str,
    days: int,
    lead_id: Optional[str] = None,
    price_currency: Optional[str] = None,
    pay_currency: Optional[str] = None,
) -> Dict[str, Any]:
    url = f"{api_base()}/payment"

    payload = {
        "price_amount": price_amount,
        "price_currency": price_currency or default_price_currency(),
        "pay_currency": pay_currency or default_pay_currency(),
        "order_id": order_id,
        "order_description": order_description,
        "ipn_callback_url": os.getenv(
            "NOWPAYMENTS_IPN_CALLBACK_URL",
            "https://api.ndsp.app/api/v6/payments/nowpayments/webhook",
        ),
    }

    response = requests.post(
        url,
        headers={
            "x-api-key": api_key(),
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=20,
    )

    try:
        data = response.json()
    except Exception:
        data = {
            "raw": response.text,
        }

    if response.status_code >= 400:
        raise NOWPaymentsError(str(data))

    return data


def get_payment(payment_id: str) -> Dict[str, Any]:
    url = f"{api_base()}/payment/{payment_id}"

    response = requests.get(
        url,
        headers={
            "x-api-key": api_key(),
        },
        timeout=20,
    )

    try:
        data = response.json()
    except Exception:
        data = {
            "raw": response.text,
        }

    if response.status_code >= 400:
        raise NOWPaymentsError(str(data))

    return data
