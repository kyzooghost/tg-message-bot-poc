from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import logging
logger = logging.getLogger(__name__)

# https://docs.python-telegram-bot.org/en/v21.1.1/examples.conversationbot.html

# TODO - Save to DynamoDB
# TODO - Loading + error state
# TODO - Clear local memory after save to DynamoDB

MESSAGE_KEY, MESSAGE_VALUE = range(2)

async def write(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation - ask to input a message key."""

    await update.message.reply_text(
        "Hi! I will save your messages. Please enter a message tag:"
    )

    return MESSAGE_KEY

async def message_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ends the conversation - ask to input a message."""

    context.user_data["message_key"] = update.message.text

    await update.message.reply_text(
        "Please enter a message:"
    )

    return MESSAGE_VALUE

async def message_value(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    context.user_data["message_value"] = update.message.text

    user = update.message.from_user
    logger.info("Message saved by %s under tag %s: %s", user.full_name, context.user_data["message_key"], context.user_data["message_value"])
    await update.message.reply_text("Thank you! Your message has been saved")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled saving a message.", user.full_name)
    await update.message.reply_text(
        "Bye!", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

handler = ConversationHandler(
    entry_points=[CommandHandler("write", write)],
    states={
        MESSAGE_KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, message_key)],
        MESSAGE_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, message_value)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)