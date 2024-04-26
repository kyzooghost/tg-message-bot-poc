from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler
import os
import logging
from handlers import fallback, help, start, cancel
from handlers.actions import (
    delete as delete_action,
    get as get_action,
    write as write_action
)
from conversation_states import SELECTING_ACTION, LIST, WRITE, GET, UPDATE, DELETE

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# https://docs.python-telegram-bot.org/en/stable/examples.nestedconversationbot.html

def main():
    TG_TOKEN = os.environ.get("TG_TOKEN")
    app = ApplicationBuilder().token(TG_TOKEN).build()

    root_conversation = ConversationHandler(
        entry_points=[CommandHandler("start", start.command_handler)],
        states={
            SELECTING_ACTION: [
                get_action.handler,
                write_action.handler,
                delete_action.handler
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel.handler)],
    )
    app.add_handler(root_conversation)

    app.add_handler(CommandHandler("help", help.handler))
    app.add_handler(MessageHandler(filters.COMMAND, fallback.handler))
    app.run_polling()

if __name__ == '__main__':
    main()