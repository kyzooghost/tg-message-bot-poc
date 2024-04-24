from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os
import logging
from handlers import fallback_command, write

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('TODO - Show all commands')

def main():
    TG_TOKEN = os.environ.get("TG_TOKEN")

    app = ApplicationBuilder().token(TG_TOKEN).build()
    app.add_handler(CommandHandler("help", help))
    app.add_handler(write.handler)
# 
    # Fallback
    app.add_handler(MessageHandler(filters.COMMAND, fallback_command.handler))
    app.run_polling()

if __name__ == '__main__':
    main()