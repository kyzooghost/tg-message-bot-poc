from telegram import (
    ReplyKeyboardRemove, 
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    Message
)
from telegram.ext import (
    CommandHandler,
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
import logging
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)
logger = logging.getLogger(__name__)

MESSAGE_KEY, MESSAGE_VALUE = range(2)
cancel_button_ui = [[InlineKeyboardButton("Cancel", callback_data="0")]]

### Helper functions

async def edit_last_message(context: ContextTypes.DEFAULT_TYPE, new_text: str = None):
    message_to_cleanup: Message | None = context.user_data.get("message_to_cleanup", None)
    if message_to_cleanup is not None:
        await message_to_cleanup.edit_text(
            message_to_cleanup.text if new_text == None else new_text,
            reply_markup=None
        )
        # await message_to_cleanup.edit_reply_markup()
        context.user_data["message_to_cleanup"] = None

def cleanup_state(context: ContextTypes.DEFAULT_TYPE):
    context.user_data["message_to_cleanup"] = None
    context.user_data["message_key"] = None
    context.user_data["message_value"] = None

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

    # State cleanup
    cleanup_state(context)
    return ConversationHandler.END

async def cancel_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel"""
    # UI
    query = update.callback_query
    # await query.delete_message()

    # Logging
    user = query.from_user
    logger.info("User %s canceled saving a message.", user.full_name)

    # State cleanup
    await query.answer()
    cleanup_state(context)

    await query.edit_message_text(start_menu.text, reply_markup=start_menu.reply_markup)
    return ConversationHandler.END

async def cancel_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    # UI
    await edit_last_message(context)
    await update.message.reply_text(
        "Bye!", reply_markup=ReplyKeyboardRemove()
    )

    # Logging
    user = update.message.from_user
    logger.info("User %s canceled saving a message.", user.full_name)

    # State cleanup
    cleanup_state(context)
    return ConversationHandler.END

handler = ConversationHandler(
    # entry_points=[CommandHandler("write", write)],
    entry_points=[CallbackQueryHandler(write, pattern="^" + str(WRITE) + "$")],
    states={
        MESSAGE_KEY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, message_key),
            CallbackQueryHandler(cancel_button)
        ],
        MESSAGE_VALUE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, message_value),
            CallbackQueryHandler(cancel_button)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel_fallback)],
    map_to_parent={
        # Return to top level menu
        ConversationHandler.END: SELECTING_ACTION,
    },
)