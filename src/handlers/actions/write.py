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
from conversation_states import SELECTING_ACTION, WRITE
from ui import start_menu
from ui.cancel_button import cancel_button_ui, cancel_button_handler
from handlers.utils.cleanup_state import cleanup_state
from handlers.utils.edit_last_message import edit_last_message
import logging
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)
logger = logging.getLogger(__name__)

MESSAGE_KEY, MESSAGE_VALUE = range(2)
user_data_keys = ["message_to_cleanup", "message_key", "message_value"]

### Handler functions

async def write(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation - ask to input a message key."""
    await update.callback_query.answer()

    # UI
    reply_message = await update.callback_query.edit_message_text(
        "Hi! I will save your messages. Please enter a message tag:",
        reply_markup=InlineKeyboardMarkup(cancel_button_ui)
    )

    # State
    context.user_data["message_to_cleanup"]=reply_message
    return MESSAGE_KEY

async def message_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ends the conversation - ask to input a message."""
    # UI
    await edit_last_message(context, f"TAG: {update.message.text}")
    reply_message = await update.message.reply_text(
        "Please enter a message:",
        reply_markup=InlineKeyboardMarkup(cancel_button_ui)
    )

    # State
    context.user_data["message_to_cleanup"]=reply_message
    context.user_data["message_key"] = update.message.text

    return MESSAGE_VALUE

async def message_value(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    # UI
    await edit_last_message(context, f"MESSAGE: {update.message.text}")
    current_message = await update.message.reply_text("Processing...")

    # State
    context.user_data["message_value"] = update.message.text

    # API call
    user = update.message.from_user
    dynamodb_client = db_context_class.DbContextClass()
    try:
        dynamodb_client.write(str(user.id), context.user_data["message_key"], context.user_data["message_value"])
        await current_message.edit_text("Thank you! Your message has been saved.")
        logger.info(
            "Message saved by user %i: '%s - %s'", 
            user.id, 
            context.user_data["message_key"], 
            context.user_data["message_value"]
        )

    except Exception as e:
        await current_message.edit_text("Something went wrong.")
        logger.error(str(e))

    await current_message.reply_text(start_menu.text, reply_markup=start_menu.reply_markup)

    # State cleanup
    cleanup_state(context, user_data_keys)
    return ConversationHandler.END

async def cancel_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await cancel_button_handler(update, context, user_data_keys)

handler = ConversationHandler(
    # entry_points=[CommandHandler("write", write)],
    entry_points=[CallbackQueryHandler(write, pattern="^" + str(WRITE) + "$")],
    states={
        MESSAGE_KEY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, message_key),
        ],
        MESSAGE_VALUE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, message_value),
        ],
    },
    fallbacks=[CallbackQueryHandler(cancel_button)],
    map_to_parent={
        # Return to top level menu
        ConversationHandler.END: SELECTING_ACTION,
    },
)