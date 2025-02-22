from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from flask import Flask, request
import os

TOKEN = os.getenv("TOKEN")  # Obtiene el token desde las variables de entorno
WEBHOOK_URL = "https://telegrambot-2o8t.onrender.com"  # Cambia esto con tu URL en Render

app = Flask(__name__)

bot_app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("¡Hola! Soy tu bot de Telegram con Webhooks.")

async def echo(update: Update, context: CallbackContext):
    await update.message.reply_text(update.message.text)

# Configurar Handlers
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    bot_app.update_queue.put(request.get_json())
    return "OK", 200

async def set_webhook():
    await bot_app.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

if __name__ == "__main__":
    import threading
    threading.Thread(target=bot_app.run_webhook, args=(f"{WEBHOOK_URL}/{TOKEN}",)).start()
    app.run(host="0.0.0.0", port=5000)
