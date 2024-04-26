
class UserMessageClass:
    def __init__(self, message_key: str, message_value: str):
        self.message_key = message_key
        self.message_value = message_value

    @classmethod
    def from_dynamodb_query_item(cls, dynamodb_query_item):
        return cls(
            message_key=dynamodb_query_item['UserMessageKey']['S'],
            message_value=dynamodb_query_item['UserMessageValue']['S'],
        )