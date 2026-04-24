import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from .handlers import start, olympiads, mood, summary

def run_bot():
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start.handle_start))
    app.add_handler(CommandHandler("olympiads", olympiads.handle_list))
    app.add_handler(CommandHandler("mood", mood.handle_mood))
    app.add_handler(CommandHandler("summary", summary.handle_summary))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start.handle_message))

    app.run_polling()


if __name__ == "__main__":
    run_bot()
