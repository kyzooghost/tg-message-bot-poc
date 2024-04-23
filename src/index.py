from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler
import os

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

def main():
    TG_TOKEN = os.environ.get("TG_TOKEN")
    app = ApplicationBuilder().token(TG_TOKEN).build()
    app.add_handler(CommandHandler("hello", hello))
    print("Bot started")
    app.run_polling()

if __name__ == '__main__':
    main()