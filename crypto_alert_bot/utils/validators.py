"""Validation helpers."""

from __future__ import annotations


def validate_price(text: str) -> float | None:
    cleaned = text.replace(",", "").strip()
    try:
        value = float(cleaned)
    except ValueError:
        return None
    if value <= 0:
        return None
    return value


def validate_coin_symbol(symbol: str) -> str | None:
    cleaned = symbol.strip().upper()
    if not cleaned or len(cleaned) > 10 or not cleaned.isalnum():
        return None
    return cleaned
