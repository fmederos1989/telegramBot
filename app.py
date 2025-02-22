from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
import asyncio

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = f"https://telegrambot-2o8t.onrender.com/{TOKEN}"  # Cambia con tu URL en Render

app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

# Handlers
async def start(update: Update, context):
    await update.message.reply_text("¡Hola! Soy tu bot en Render.")

async def echo(update: Update, context):
    await update.message.reply_text(update.message.text)

bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        update_json = request.get_json(force=True)
        update = Update.de_json(update_json, bot_app.bot)
        asyncio.create_task(bot_app.process_update(update))  # Maneja el evento en segundo plano
        return "OK", 200
    except Exception as e:
        print(f"❌ ERROR en webhook: {e}")
        return "Internal Server Error", 500  # Devuelve código 500 si hay un error

async def set_webhook():
    success = await bot_app.bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook configurado en {WEBHOOK_URL}: {success}")

async def main():
    await set_webhook()
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    asyncio.run(main())
