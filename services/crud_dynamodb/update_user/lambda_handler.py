import json

import json
import os

import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE')
table = dynamodb.Table(table_name)


def update_user(event, context):
    body = json.loads(event.get('body'))
    user_id = event['pathParameters']['id']
    response = table.update_item(
        Key={'id': user_id},
        ExpressionAttributeValues={
          ":username": body.get('username'),
          ":city": body.get('city'),
          ":email": body.get('email'),
          ":first_name": body.get('first_name'),
          ":last_name": body.get('last_name'),
        },
        UpdateExpression=("SET username = :username, city = :city, email = :email, first_name = :first_name, "
                          "last_name = :last_name"),
        ReturnValues="ALL_NEW",
    )
    return {
        'statusCode': 200,
        'body': json.dumps(response.get('Attributes'))
    }
