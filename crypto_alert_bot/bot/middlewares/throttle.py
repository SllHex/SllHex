"""Simple anti-spam middleware."""

from __future__ import annotations

import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache


class ThrottleMiddleware(BaseMiddleware):
    """Allow at most one message per user per configured interval."""

    def __init__(self, period: float = 0.5) -> None:
        super().__init__()
        self.period = period
        self._cache: TTLCache[int, float] = TTLCache(maxsize=10000, ttl=period)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user = event.from_user
        if user is None:
            return await handler(event, data)

        now = time.monotonic()
        last_ts = self._cache.get(user.id)
        if last_ts is not None and (now - last_ts) < self.period:
            return None

        self._cache[user.id] = now
        return await handler(event, data)
