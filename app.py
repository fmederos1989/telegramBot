from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "7630813785:AAGPJZyCz6aJ8HBhk1IM0UO1AN7MTMjhnWk"


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("¡Hola! Soy tu bot de Telegram.")


async def echo(update: Update, context: CallbackContext):
    await update.message.reply_text(update.message.text)


def main():
    app = Application.builder().token(TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Iniciar el bot
    print("Bot iniciado...")
    app.run_polling()


if __name__ == "__main__":
    main()
