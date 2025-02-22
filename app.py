from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
import asyncio


TOKEN = os.getenv("TOKEN")  # Token del bot
WEBHOOK_URL = "https://telegrambot-2o8t.onrender.com"  # Reemplaza con la URL de tu Render

app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

# Handlers
async def start(update: Update, context):
    await update.message.reply_text("¡Hola! Soy tu bot de Telegram con Webhooks.")

async def echo(update: Update, context):
    await update.message.reply_text(update.message.text)

bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(), bot_app.bot)
    await bot_app.process_update(update)
    return "OK", 200

async def set_webhook():
    await bot_app.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

async def main():
    await set_webhook()
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    asyncio.run(main())
