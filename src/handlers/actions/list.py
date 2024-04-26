from telegram import (
    Update, 
    Message,
)
from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler
)
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning
from classes import db_context_class
from conversation_states import SELECTING_ACTION, LIST
from ui import start_menu
import logging
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)
logger = logging.getLogger(__name__)

### Handler functions

async def list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    # UI
    last_message: Message = await update.callback_query.edit_message_text("Retrieving messages...")

    # API call
    user = update.callback_query.from_user
    dynamodb_client = db_context_class.DbContextClass()
    try:
        messages = dynamodb_client.list(str(user.id))
        if len(messages) == 0:
            await last_message.edit_text("No messages found")
        else:
            list_ui = ["TAG: MESSAGE", "------------"]
            for message in messages:
                list_ui.append(f"{message.message_key}: {message.message_value}")
            await last_message.edit_text("\n".join(list_ui))
    except Exception as e:
        await last_message.edit_text("Something went wrong")
        logger.error(f"Error: {str(e)}")

    await last_message.reply_text(start_menu.text, reply_markup=start_menu.reply_markup)
    return SELECTING_ACTION

handler = CallbackQueryHandler(list, pattern="^" + str(LIST) + "$")