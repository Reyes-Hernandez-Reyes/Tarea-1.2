import logging
import re

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Expresión regular para detectar mensajes que contienen "Hola"
expresion_regular = re.compile(r"hello|hi|hey|hola", re.IGNORECASE)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message if it matches the regular expression."""
    message_text = update.message.text
    if expresion_regular.search(message_text):
        await update.message.reply_text("¡Hola! ¿Cómo estás?")
    else:
        await update.message.reply_text("No entendí tu mensaje.")


def main() -> None:
    """Start the bot."""
    application = Application.builder().token("7144495527:AAEDMWjdja2fhxc-AjmwbEWsZ_3P8_nuhmg").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()