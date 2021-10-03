import json
import os
import uuid

import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE')
table = dynamodb.Table(table_name)


def create_user(event, context):
    body = json.loads(event.get('body'))
    if not body.get('id'):
        body['id'] = str(uuid.uuid4())
    user = {
        'id': body.get('id'),
        'username': body.get('username'),
        'city': body.get('city'),
        'email': body.get('email'),
        'first_name': body.get('first_name'),
        'last_name': body.get('last_name'),
    }
    table.put_item(Item=user)
    return {
        'statusCode': 201,
        'body': json.dumps(user)
    }
