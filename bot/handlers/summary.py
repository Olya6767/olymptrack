import httpx
from telegram import Update
from telegram.ext import ContextTypes
from datetime import date, timedelta

API_BASE = "http://localhost:5000/api"


async def handle_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    today = date.today()
    in_a_week = today + timedelta(days=7)
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/olympiads/", params={"user_id": user_id})
    items = resp.json() if resp.status_code == 200 else []
    upcoming = [
        o for o in items
        if o["deadline"] and today.isoformat() <= o["deadline"] <= in_a_week.isoformat()
    ]
    lines = [f"Доброе утро! Сегодня {today.strftime('%d.%m.%Y')}"]
    if upcoming:
        lines.append("Ближайшие дедлайны:")
        for o in upcoming:
            days_left = (date.fromisoformat(o["deadline"]) - today).days
            lines.append(f"  - {o['name']}: через {days_left} дн.")
    else:
        lines.append("Ближайших дедлайнов нет.")
    await update.message.reply_text("\n".join(lines))
