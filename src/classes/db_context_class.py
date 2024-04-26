import boto3
import os
from typing import Union
import logging
logger = logging.getLogger(__name__)

class DbContextClass:
    def __init__(self):
        self.dynamodb_client = boto3.client(
            'dynamodb', 
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name='us-west-2'
        )
        self.table_name = os.environ.get('DYNAMODB_TABLE_NAME')

    def write(self, userId: str, userMessageKey: str, userMessageValue: str):
        self.dynamodb_client.put_item(
            TableName=self.table_name,
            Item={
                'UserId': {'S': userId},
                'UserMessageKey': {'S': userMessageKey},
                'UserMessageValue': {'S': userMessageValue}
            }
        )

    def get(self, userId: str, userMessageKey: str) -> Union[str, None]:
        resp = self.dynamodb_client.get_item(
            TableName=self.table_name,
            Key={
                'UserId': {'S': userId},
                'UserMessageKey': {'S': userMessageKey}
            }
        )

        if 'Item' in resp:
            return resp['Item']['UserMessageValue']['S']
        else:
            return None

    # Return 'true' if item was deleted, 'false' if item not present
    def delete(self, userId: str, userMessageKey: str) -> bool:
        # Contrary to documentation, delete_item response does not provide any information on whether an item was deleted or not
        item = self.get(userId, userMessageKey)
        if item is None:
            return False
        else:
            self.dynamodb_client.delete_item(
                TableName=self.table_name,
                Key={
                    'UserId': {'S': userId},
                    'UserMessageKey': {'S': userMessageKey}
                }
            )
            return True
        
    # Return 'true' if item was deleted, 'false' if item not present
    def update(self, userId: str, userMessageKey: str, userMessageValue: str) -> bool:
        item = self.get(userId, userMessageKey)
        if item is None:
            return False
        else:
            self.dynamodb_client.update_item(
                TableName=self.table_name,
                Key={
                    'UserId': {'S': userId},
                    'UserMessageKey': {'S': userMessageKey},
                },
                AttributeUpdates={
                    'UserMessageValue': {'Value': {'S': userMessageValue}}
                }
            )
            return True