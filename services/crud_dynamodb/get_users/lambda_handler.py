import json
import os

import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE')
table = dynamodb.Table(table_name)


def get_users(event, context):
    result = table.scan()
    return {
        'statusCode': 200,
        'body': json.dumps(result.get('Items'))
    }
