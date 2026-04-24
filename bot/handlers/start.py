from telegram import Update
from telegram.ext import ContextTypes


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я OlympTrack — твой помощник для олимпиад.\n\n"
        "Команды:\n"
        "/olympiads — список олимпиад\n"
        "/mood — записать настроение\n"
        "/summary — утренняя сводка"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Используй команды для работы с ботом. /start — список команд.")
