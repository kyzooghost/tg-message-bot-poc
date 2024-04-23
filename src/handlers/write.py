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

MESSAGE_KEY, MESSAGE_VALUE = range(2)

async def write(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation - ask to input a message key."""

    await update.message.reply_text(
        "Hi! I will save your messages. Please enter a message tag:"
    )

    return MESSAGE_KEY

async def message_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation - ask to input a message key."""

    await update.message.reply_text(
        "Please enter a message:"
    )

    return MESSAGE_VALUE

async def message_value(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text("Thank you! Your message has been saved")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
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

# async def write(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # await update.message.reply_text(f'Hello {update.effective_user.first_name}')

# async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")