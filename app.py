from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
import asyncio

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = f"https://tu-app.onrender.com/{TOKEN}"  # Cambia con tu URL en Render

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
async def webhook():
    """Maneja las actualizaciones de Telegram."""
    try:
        update_json = request.get_json(force=True)
        update = Update.de_json(update_json, bot_app.bot)

        # ✅ Se usa `await` correctamente
        await bot_app.process_update(update)

        return "OK", 200
    except Exception as e:
        print(f"❌ ERROR en webhook: {e}")
        return "Internal Server Error", 500


async def set_webhook():
    """Configura el webhook en Telegram."""
    success = await bot_app.bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook configurado en {WEBHOOK_URL}: {success}")


async def main():
    await set_webhook()
    print("🚀 Bot iniciado correctamente")
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    asyncio.run(main())
