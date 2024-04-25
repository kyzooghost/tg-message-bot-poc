from telegram.ext import ContextTypes
from typing import List

def cleanup_state(context: ContextTypes.DEFAULT_TYPE, keys_to_cleanup: List[str]):
    for key in keys_to_cleanup:
        context.user_data[key] = None