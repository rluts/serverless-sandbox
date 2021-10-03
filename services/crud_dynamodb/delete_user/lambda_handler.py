import os
import boto3


dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE')
table = dynamodb.Table(table_name)


def delete_user(event, context):
    user_id = event['pathParameters']['id']
    table.delete_item(Key={'id': user_id})
    return {
        'statusCode': 204,
    }
