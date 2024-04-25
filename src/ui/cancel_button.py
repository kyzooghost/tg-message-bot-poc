from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from typing import List
from ui import start_menu
from handlers.utils.cleanup_state import cleanup_state

cancel_button_ui = [[InlineKeyboardButton("Cancel", callback_data="0")]]

async def cancel_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data_keys: List[str]) -> int:
    """Cancel"""
    # State cleanup
    query = update.callback_query
    await query.answer()
    cleanup_state(context, user_data_keys)

    # UI
    await query.edit_message_text(start_menu.text, reply_markup=start_menu.reply_markup)
    return ConversationHandler.END