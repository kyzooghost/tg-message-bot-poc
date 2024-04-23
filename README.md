POC Telegram as frontend

Starting message
Save and retrieve messages (stored in DynamoDB) by name

`/write` - Write message under a tag

`/read` - Read message under a tag

`/list` - See all messages

`/update` - Update message under a tag

`/delete` - Delete message under a tag

?ConversationHandler
- Command -> Start 'mode', next response = end of mode
- Use callbackdata cache
- https://github.com/python-telegram-bot/python-telegram-bot/wiki/Arbitrary-callback_data
- https://stackoverflow.com/questions/34457568/how-to-show-options-in-telegram-bot

Resoures
- https://docs.python-telegram-bot.org/en/stable/telegram.at-tree.html
- https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API
- https://core.telegram.org/bots/api#using-a-local-bot-api-server