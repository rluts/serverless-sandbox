import json
import os
import uuid

import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE')
table = dynamodb.Table(table_name)


def sqs_dynamodb(event, context):
    for item in event.get('Records', []):
        body = json.loads(item.get('body', '{}'))
        user = {
            'id': str(uuid.uuid4()),
            'username': body.get('username'),
            'city': body.get('city'),
            'email': body.get('email'),
            'first_name': body.get('first_name'),
            'last_name': body.get('last_name'),
        }
        table.put_item(Item=user)

