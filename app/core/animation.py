from __future__ import annotations

import asyncio

from aiogram.types import Message

GREEN_BLOCK = "🟩"
EMPTY_BLOCK = "⬜"


async def animate_green_progress(
    message: Message,
    title: str = "Processing your order",
    steps: int = 10,
    delay: float = 0.2,
) -> None:
    """Animate a green progress bar by editing one Telegram message."""
    for current_step in range(1, steps + 1):
        filled = GREEN_BLOCK * current_step
        empty = EMPTY_BLOCK * (steps - current_step)
        percent = current_step * int(100 / steps)
        bar = f"{filled}{empty}"
        await message.edit_text(f"{title}...\n\n{bar} {percent}%")
        await asyncio.sleep(delay)
