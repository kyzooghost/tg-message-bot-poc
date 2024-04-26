
from telegram import Message
from telegram.ext import ContextTypes
from typing import Union

async def edit_last_message(context: ContextTypes.DEFAULT_TYPE, new_text: str = None) -> Union[Message, None]:
    message_to_cleanup: Message | None = context.user_data.get("message_to_cleanup", None)
    if message_to_cleanup is not None:
        await message_to_cleanup.edit_text(
            message_to_cleanup.text if new_text == None else new_text,
            reply_markup=None
        )
        context.user_data["message_to_cleanup"] = None
    return message_to_cleanup
