import boto3
import os

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

    def get(self, userId: str, userMessageKey: str):
        self.dynamodb_client.get_item(
            TableName=self.table_name,
            Key={
                'UserId': {'S': userId},
                'UserMessageKey': {'S': userMessageKey}
            }
        )

    def delete(self, userId: str, userMessageKey: str):
        self.dynamodb_client.delete_item(
            TableName=self.table_name,
            Key={
                'UserId': {'S': userId},
                'UserMessageKey': {'S': userMessageKey}
            }
        )