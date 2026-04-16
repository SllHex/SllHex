"""Formatting helpers."""

from __future__ import annotations


def format_price(price: float) -> str:
    if abs(price) >= 1:
        return f"${price:,.2f}"
    return f"${price:,.6f}"


def format_percentage(pct: float) -> str:
    emoji = "📈" if pct >= 0 else "📉"
    sign = "+" if pct >= 0 else ""
    return f"{emoji} {sign}{pct:.2f}%"


def format_alert_list(alerts: list[dict], current_prices: dict[str, float]) -> str:
    if not alerts:
        return "You do not have active alerts yet."

    lines = ["⚠️ <b>Your Active Alerts</b>"]
    for idx, alert in enumerate(alerts, 1):
        current = current_prices.get(alert["coin_id"])
        target = float(alert["target_price"])
        away_text = "N/A"
        current_text = "Unavailable"
        if current is not None:
            current_text = format_price(current)
            diff_pct = ((current - target) / target) * 100 if target else 0.0
            away_text = f"{diff_pct:+.2f}%"

        lines.append(
            (
                f"\n{idx}) <b>{alert['coin_symbol']}</b> ({alert['coin_id']})\n"
                f"• Target: {format_price(target)}\n"
                f"• Direction: <b>{alert['direction'].upper()}</b>\n"
                f"• Current: {current_text}\n"
                f"• Distance to target: {away_text}"
            )
        )

    return "\n".join(lines)
