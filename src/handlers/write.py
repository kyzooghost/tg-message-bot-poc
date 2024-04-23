from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def write(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')