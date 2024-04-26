from telegram import (
    Update, 
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning
from classes import db_context_class
from conversation_states import SELECTING_ACTION, DELETE
from handlers.utils.cleanup_state import cleanup_state
from handlers.utils.edit_last_message import edit_last_message
from ui import start_menu
from ui.cancel_button import cancel_button_ui, cancel_button_handler
import logging
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)
logger = logging.getLogger(__name__)

MESSAGE_KEY = range(1)
user_data_keys = ["message_to_cleanup"]

### Handler functions

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation - ask to input a message key."""
    await update.callback_query.answer()

    # UI
    reply_message = await update.callback_query.edit_message_text(
        "Please enter the tag for the message you wish to delete:",
        reply_markup=InlineKeyboardMarkup(cancel_button_ui)
    )

    # State
    context.user_data["message_to_cleanup"]=reply_message
    return MESSAGE_KEY

async def message_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ends the conversation - ask to input a message."""

    # Loading UI
    last_message = await edit_last_message(context, "Deleting message...")
    
    # API call
    user = update.message.from_user
    dynamodb_client = db_context_class.DbContextClass()

    try: 
        is_delete_done = dynamodb_client.delete(str(user.id), update.message.text)
        if is_delete_done == True:
            await last_message.edit_text("Deleted message!")
        else:
            await last_message.edit_text("Message not found.")
    except Exception as e:
        await last_message.edit_text("Something went wrong.")
        logger.error(f"Error: {str(e)}")

    # UI
    await update.message.reply_text(start_menu.text, reply_markup=start_menu.reply_markup)

    # State
    cleanup_state(context, user_data_keys)
    return ConversationHandler.END

async def cancel_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await cancel_button_handler(update, context, user_data_keys)

handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(delete, pattern="^" + str(DELETE) + "$")],
    states={
        MESSAGE_KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, message_key)],
    },
    fallbacks=[CallbackQueryHandler(cancel_button)],
    map_to_parent={
        # Return to top level menu
        ConversationHandler.END: SELECTING_ACTION,
    },
)