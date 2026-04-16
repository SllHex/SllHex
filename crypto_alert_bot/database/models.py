"""Database model helpers."""

from typing import TypedDict


class Alert(TypedDict):
    id: int
    user_id: int
    coin_id: str
    coin_symbol: str
    target_price: float
    direction: str
    created_at: str
    is_active: int
