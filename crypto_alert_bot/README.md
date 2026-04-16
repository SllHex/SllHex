# Crypto Price Alert Bot (aiogram 3.x)

A fully modular Telegram bot for creating crypto price alerts.

## Features
- Async Telegram bot using `aiogram 3.x`
- Async SQLite persistence with `aiosqlite`
- Async CoinGecko integration with `aiohttp`
- FSM-based multi-step alert creation
- Background alert checker with safe infinite loop
- Admin tools: `/stats`, `/broadcast`
- Rate limiting middleware

## Project structure

```text
crypto_alert_bot/
├── main.py
├── .env
├── requirements.txt
├── config/
├── bot/
├── handlers/
├── services/
├── database/
├── keyboards/
└── utils/
```

## Setup
1. Create and activate a virtualenv.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` from `.env.example` and fill values.
4. Run:
   ```bash
   python main.py
   ```

## Notes
- Do not commit `.env`.
- The checker deactivates triggered alerts instead of deleting them.
- CoinGecko free API rate limits are mitigated by grouping alerts by coin.
