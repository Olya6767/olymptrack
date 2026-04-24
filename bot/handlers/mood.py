from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, CommandHandler, filters
import httpx
from datetime import date

WAITING_SCORE = 1
API_BASE = "http://localhost:5000/api"


async def handle_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Оцени своё настроение от 1 до 5:")
    return WAITING_SCORE


async def receive_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 5):
        await update.message.reply_text("Введи число от 1 до 5.")
        return WAITING_SCORE
    score = int(text)
    user_id = update.effective_user.id
    async with httpx.AsyncClient() as client:
        await client.post(f"{API_BASE}/mood/", json={
            "user_id": user_id,
            "date": str(date.today()),
            "score": score,
        })
    await update.message.reply_text(f"Записал настроение: {score}/5")
    return ConversationHandler.END


mood_conversation = ConversationHandler(
    entry_points=[CommandHandler("mood", handle_mood)],
    states={WAITING_SCORE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_score)]},
    fallbacks=[],
)
