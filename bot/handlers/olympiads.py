import httpx
from telegram import Update
from telegram.ext import ContextTypes

API_BASE = "http://localhost:5000/api"


async def handle_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/olympiads/", params={"user_id": user_id})
    if resp.status_code != 200:
        await update.message.reply_text("Ошибка при получении олимпиад.")
        return
    items = resp.json()
    if not items:
        await update.message.reply_text("Олимпиад пока нет.")
        return
    lines = [f"{o['name']} — {o['status']} (дедлайн: {o['deadline'] or '—'})" for o in items]
    await update.message.reply_text("\n".join(lines))
