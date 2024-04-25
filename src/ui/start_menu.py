from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from conversation_states import LIST, WRITE, GET, UPDATE, DELETE

_keyboard = [
    [InlineKeyboardButton("Get all messages", callback_data=str(LIST))],
    [InlineKeyboardButton("Write message", callback_data=str(WRITE))],
    [InlineKeyboardButton("Get message", callback_data=str(GET))],
    [InlineKeyboardButton("Update message", callback_data=str(UPDATE))],
    [InlineKeyboardButton("Delete message", callback_data=str(DELETE))],
]

reply_markup = InlineKeyboardMarkup(_keyboard)
text = "Choose an action"