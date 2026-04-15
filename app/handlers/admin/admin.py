from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.repositories.store_repo import StoreRepository

router = Router()


def register_admin_handlers(repo: StoreRepository, admin_ids: list[int]) -> Router:
    def is_admin(user_id: int | None) -> bool:
        return bool(user_id and user_id in admin_ids)

    @router.message(Command("admin"))
    async def admin_panel(message: Message) -> None:
        user_id = message.from_user.id if message.from_user else None
        if not is_admin(user_id):
            await message.answer("⛔ You are not authorized to access admin panel.")
            return

        await message.answer(
            "⚙️ *Admin Panel*\n"
            "Use command below to add product:\n"
            "`/addproduct name|description|price|stock`",
            parse_mode="Markdown",
        )

    @router.message(Command("addproduct"))
    async def add_product(message: Message) -> None:
        user_id = message.from_user.id if message.from_user else None
        if not is_admin(user_id):
            await message.answer("⛔ Admin only.")
            return

        payload = (message.text or "").replace("/addproduct", "", 1).strip()
        parts = [part.strip() for part in payload.split("|")]
        if len(parts) != 4:
            await message.answer("Usage: `/addproduct name|description|price|stock`", parse_mode="Markdown")
            return

        name, description, price_raw, stock_raw = parts
        if not (price_raw.isdigit() and stock_raw.isdigit()):
            await message.answer("Price and stock must be numeric.")
            return

        product_id = repo.create_product(name, description, int(price_raw), int(stock_raw))
        await message.answer(f"✅ Product created with ID `{product_id}`", parse_mode="Markdown")

    return router
