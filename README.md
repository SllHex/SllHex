# NovaStore Telegram Bot (Modular Demo)

A clean, modular **Telegram shopping bot** built with **Python + aiogram 3** for employer demos.

## Highlights

- Modular architecture (`handlers`, `services`, `repositories`, `db`, `keyboards`)
- English UX copy for professional showcase
- Demo-ready shopping flow: catalog → cart → checkout
- **Animated green progress bar** during checkout
- Admin command to add products live in Telegram
- SQLite persistence for easy local run

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# set BOT_TOKEN and ADMIN_IDS in .env
python -m app.bot
```

## User commands

- `/start` - welcome and menu
- `/catalog` - list products
- `/add <product_id>` - add product to cart
- `/cart` - show cart
- `/checkout` - mock payment + green animation

## Admin commands

- `/admin`
- `/addproduct name|description|price|stock`

## Green progress animation

During `/checkout`, the bot edits a single message with a filling green bar:

```text
🟢 Secure payment in progress...
🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜ 50%
```

This makes the bot feel dynamic and visually impressive for employer testing.
