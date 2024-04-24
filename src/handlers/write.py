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
import logging
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)
logger = logging.getLogger(__name__)

# https://docs.python-telegram-bot.org/en/v21.1.1/examples.conversationbot.html

# TODO - Save to DynamoDB
# TODO - Loading + error state

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

    # UI
    reply_message = await update.message.reply_text(
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
    await update.message.reply_text("Thank you! Your message has been saved.")

    # State
    context.user_data["message_value"] = update.message.text

    # Logging
    user = update.message.from_user
    logger.info("Message saved by %s under tag %s: %s", user.full_name, context.user_data["message_key"], 
    context.user_data["message_value"])

    # State cleanup
    cleanup_state(context)
    return ConversationHandler.END

async def cancel_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel"""
    # UI
    query = update.callback_query
    await query.delete_message()

    # Logging
    user = query.from_user
    logger.info("User %s canceled saving a message.", user.full_name)

    # State cleanup
    await query.answer()
    cleanup_state(context)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
    entry_points=[CommandHandler("write", write)],
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
    fallbacks=[CommandHandler("cancel", cancel)]
)