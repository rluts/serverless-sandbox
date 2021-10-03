import json
import os

import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE')
table = dynamodb.Table(table_name)


def get_user(event, context):
    user_id = event['pathParameters']['id']
    response = table.get_item(Key={'id': user_id})
    return {
        'statusCode': 200,
        'body': json.dumps(response.get('Item'))
    }