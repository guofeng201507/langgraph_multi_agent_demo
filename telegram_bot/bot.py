import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
from langgraph_app import process_user_message

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_DEV_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("欢迎使用 LangGraph 多智能体 Bot！请输入你的问题。")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        response = process_user_message(user_input)
    except Exception as e:
        logging.exception("Error processing message")
        response = "对不起，处理出错了。"

    await update.message.reply_text(response)


if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
