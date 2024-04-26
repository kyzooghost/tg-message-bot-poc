from telegram import Update
from telegram.ext import ContextTypes
from conversation_states import SELECTING_ACTION
from ui import start_menu

async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(start_menu.text, reply_markup=start_menu.reply_markup)
    return SELECTING_ACTION

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(start_menu.text, reply_markup=start_menu.reply_markup)
    return SELECTING_ACTION