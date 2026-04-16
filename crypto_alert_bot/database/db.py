"""Async SQLite utilities for alerts."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import aiosqlite

from config.settings import DB_PATH


async def _connect() -> aiosqlite.Connection:
    db_file = Path(DB_PATH)
    if not db_file.is_absolute():
        db_file = Path(__file__).resolve().parent.parent / db_file
    os.makedirs(db_file.parent, exist_ok=True)
    conn = await aiosqlite.connect(db_file)
    conn.row_factory = aiosqlite.Row
    return conn


async def init_db() -> None:
    async with await _connect() as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                coin_id TEXT NOT NULL,
                coin_symbol TEXT NOT NULL,
                target_price REAL NOT NULL,
                direction TEXT NOT NULL CHECK(direction IN ('above', 'below')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
            """
        )
        await db.commit()


async def add_alert(
    user_id: int,
    coin_id: str,
    coin_symbol: str,
    target_price: float,
    direction: str,
) -> int:
    async with await _connect() as db:
        cur = await db.execute(
            """
            INSERT INTO alerts (user_id, coin_id, coin_symbol, target_price, direction)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, coin_id, coin_symbol, target_price, direction),
        )
        await db.commit()
        return int(cur.lastrowid)


async def get_user_alerts(user_id: int) -> list[dict[str, Any]]:
    async with await _connect() as db:
        cur = await db.execute(
            """
            SELECT * FROM alerts
            WHERE user_id = ? AND is_active = 1
            ORDER BY created_at DESC
            """,
            (user_id,),
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def get_all_active_alerts() -> list[dict[str, Any]]:
    async with await _connect() as db:
        cur = await db.execute(
            "SELECT * FROM alerts WHERE is_active = 1 ORDER BY id ASC"
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def delete_alert(alert_id: int, user_id: int) -> bool:
    async with await _connect() as db:
        cur = await db.execute(
            "DELETE FROM alerts WHERE id = ? AND user_id = ?",
            (alert_id, user_id),
        )
        await db.commit()
        return cur.rowcount > 0


async def deactivate_alert(alert_id: int) -> None:
    async with await _connect() as db:
        await db.execute("UPDATE alerts SET is_active = 0 WHERE id = ?", (alert_id,))
        await db.commit()


async def count_user_alerts(user_id: int) -> int:
    async with await _connect() as db:
        cur = await db.execute(
            "SELECT COUNT(*) AS total FROM alerts WHERE user_id = ? AND is_active = 1",
            (user_id,),
        )
        row = await cur.fetchone()
        return int(row["total"]) if row else 0


async def get_admin_stats() -> dict[str, Any]:
    async with await _connect() as db:
        total_users_row = await (await db.execute(
            "SELECT COUNT(DISTINCT user_id) AS total_users FROM alerts"
        )).fetchone()
        total_alerts_row = await (await db.execute(
            "SELECT COUNT(*) AS total_alerts FROM alerts WHERE is_active = 1"
        )).fetchone()
        coins = await (
            await db.execute(
                """
                SELECT coin_symbol, COUNT(*) AS cnt
                FROM alerts
                WHERE is_active = 1
                GROUP BY coin_symbol
                ORDER BY cnt DESC
                LIMIT 3
                """
            )
        ).fetchall()

    return {
        "total_users": int(total_users_row["total_users"]) if total_users_row else 0,
        "total_active_alerts": int(total_alerts_row["total_alerts"]) if total_alerts_row else 0,
        "top_coins": [dict(c) for c in coins],
    }


async def get_all_unique_users() -> list[int]:
    async with await _connect() as db:
        rows = await (
            await db.execute("SELECT DISTINCT user_id FROM alerts ORDER BY user_id")
        ).fetchall()
    return [int(r["user_id"]) for r in rows]
