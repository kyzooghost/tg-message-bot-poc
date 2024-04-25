from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End Conversation by command."""
    await update.message.reply_text("Okay, bye")
    return ConversationHandler.END