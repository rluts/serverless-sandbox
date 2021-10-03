import json
import os
import uuid

import boto3
from itertools import islice, chain


BATCH_SIZE = 10

sqs = boto3.client('sqs')
s3 = boto3.resource('s3')
sqs_url = os.environ.get('QUEUE_URL')


def chunks(object_list, chunk_size=BATCH_SIZE):
    iterator = iter(object_list)
    while True:
        chunk = list(islice(iterator, chunk_size))
        if not chunk:
            break
        yield chunk


def read_json(bucket, file_name):
    s3_object = s3.Object(bucket, file_name)
    file_content = s3_object.get()['Body'].read().decode('utf-8')
    return json.loads(file_content)


def s3_sqs(event, context):
    json_contents = map(lambda x: read_json(x['s3']['bucket']['name'], x['s3']['object']['key']), event['Records'])
    for chunk in chunks(chain(*json_contents)):
        sqs.send_message_batch(
            Entries=[{
                'Id': str(uuid.uuid4()),
                'MessageBody': json.dumps(item),
            } for item in chunk],
            QueueUrl=sqs_url
        )
