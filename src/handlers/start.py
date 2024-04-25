from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from conversation_states import SELECTING_ACTION, LIST, WRITE, GET, UPDATE, DELETE

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [InlineKeyboardButton("Get all messages", callback_data=str(LIST))],
        [InlineKeyboardButton("Write message", callback_data=str(WRITE))],
        [InlineKeyboardButton("Get message", callback_data=str(GET))],
        [InlineKeyboardButton("Update message", callback_data=str(UPDATE))],
        [InlineKeyboardButton("Delete message", callback_data=str(DELETE))],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Choose an action", reply_markup=reply_markup)
    return SELECTING_ACTION