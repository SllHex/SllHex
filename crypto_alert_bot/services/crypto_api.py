"""CoinGecko API client helpers."""

from __future__ import annotations

import asyncio
from typing import Any

import aiohttp

from config.settings import COINGECKO_BASE_URL

_TIMEOUT = aiohttp.ClientTimeout(total=10)


async def _get_json(path: str, params: dict[str, Any]) -> Any:
    url = f"{COINGECKO_BASE_URL}{path}"
    try:
        async with aiohttp.ClientSession(timeout=_TIMEOUT) as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return None


async def get_price(coin_id: str) -> float | None:
    data = await _get_json(
        "/simple/price", {"ids": coin_id, "vs_currencies": "usd"}
    )
    if not isinstance(data, dict):
        return None
    coin_data = data.get(coin_id)
    if not isinstance(coin_data, dict):
        return None
    price = coin_data.get("usd")
    return float(price) if isinstance(price, (int, float)) else None


async def search_coin(query: str) -> list[dict[str, str]] | None:
    data = await _get_json("/search", {"query": query})
    if not isinstance(data, dict):
        return None

    coins = data.get("coins", [])
    result: list[dict[str, str]] = []
    for item in coins[:5]:
        if not isinstance(item, dict):
            continue
        coin_id = item.get("id")
        symbol = item.get("symbol")
        name = item.get("name")
        if all(isinstance(v, str) for v in [coin_id, symbol, name]):
            result.append({"id": coin_id, "symbol": symbol.upper(), "name": name})
    return result


async def get_top_coins(limit: int = 10) -> list[dict[str, Any]] | None:
    data = await _get_json(
        "/coins/markets",
        {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
        },
    )
    if not isinstance(data, list):
        return None

    results: list[dict[str, Any]] = []
    for coin in data:
        if not isinstance(coin, dict):
            continue
        results.append(
            {
                "id": coin.get("id"),
                "symbol": str(coin.get("symbol", "")).upper(),
                "name": coin.get("name"),
                "current_price": coin.get("current_price"),
                "price_change_percentage_24h": coin.get("price_change_percentage_24h"),
            }
        )
    return results
