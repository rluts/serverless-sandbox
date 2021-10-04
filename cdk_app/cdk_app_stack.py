from aws_cdk import (
    core as cdk,
    aws_dynamodb as dynamodb,
    aws_lambda_event_sources as event_sources,
    aws_s3 as s3,
    aws_sqs as sqs,
    aws_lambda,
    aws_apigateway as api
)


class CdkAppStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        table_name = 'serverless_users'

        table = dynamodb.Table(
            self, 'ItemsTable',
            table_name=table_name,
            partition_key=dynamodb.Attribute(
                name=f'id',
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY  # NOT recommended for production code
        )

        dead_letter_queue = sqs.Queue(self, 'S3DeadLetterQueue', queue_name='S3DeadLetterQueue')
        queue = sqs.Queue(
            self,
            'S3Queue',
            queue_name='S3Queue',
            dead_letter_queue=sqs.DeadLetterQueue(queue=dead_letter_queue, max_receive_count=5)
        )
        bucket = s3.Bucket(self, 'rluts-users-bucket')

        get_users_lambda = self.create_lambda(
            name='getUsers',
            handler='lambda_handler.get_users',
            path='services/crud_dynamodb/get_users',
            table=table,
        )
        get_user_lambda = self.create_lambda(
            name='getUser',
            handler='lambda_handler.get_user',
            path='services/crud_dynamodb/get_user',
            table=table,
        )
        create_user_lambda = self.create_lambda(
            name='createUser',
            handler='lambda_handler.create_user',
            path='services/crud_dynamodb/create_user',
            table=table,
        )
        update_user_lambda = self.create_lambda(
            name='updateUser',
            handler='lambda_handler.update_user',
            path='services/crud_dynamodb/update_user',
            table=table,
        )
        delete_user_lambda = self.create_lambda(
            name='deleteUser',
            handler='lambda_handler.delete_user',
            path='services/crud_dynamodb/delete_user',
            table=table,
        )
        s3_sqs_lambda = self.create_lambda(
            name='s3SQS',
            handler='lambda_handler.s3_sqs',
            path='services/s3_sqs',
            queue=queue,
            bucket=bucket
        )
        sqs_dynamodb_lambda = self.create_lambda(
            name='sqsDynamodb',
            handler='lambda_handler.sqs_dynamodb',
            path='services/sqs_dynamodb',
        )

        rest_api = api.RestApi(self, 'serverless_training_p1')
        list_rest_api_resource = rest_api.root.add_resource('user')
        get_rest_api_resource = list_rest_api_resource.add_resource('{id}')

        get_users_lambda_integration = api.LambdaIntegration(get_users_lambda)
        get_user_lambda_integration = api.LambdaIntegration(get_user_lambda)
        create_user_lambda_integration = api.LambdaIntegration(create_user_lambda)
        update_user_lambda_integration = api.LambdaIntegration(update_user_lambda)
        delete_user_lambda_integration = api.LambdaIntegration(delete_user_lambda)

        list_rest_api_resource.add_method('GET', get_users_lambda_integration)
        list_rest_api_resource.add_method('POST', create_user_lambda_integration)
        get_rest_api_resource.add_method('GET', get_user_lambda_integration)
        get_rest_api_resource.add_method('PUT', update_user_lambda_integration)
        get_rest_api_resource.add_method('DELETE', delete_user_lambda_integration)

        s3_sqs_lambda.add_event_source(
            event_sources.S3EventSource(bucket=bucket, events=[s3.EventType.OBJECT_CREATED])
        )
        sqs_dynamodb_lambda.add_event_source(
            event_sources.SqsEventSource(queue=queue)
        )

    def create_lambda(
            self,
            name,
            handler,
            path,
            table: dynamodb.Table = None,
            queue: sqs.Queue = None,
            bucket: s3.Bucket = None
    ):
        lambda_function = aws_lambda.Function(
            self,
            id=name,
            function_name=name,
            handler=handler,
            code=aws_lambda.Code.from_asset(path),
            runtime=aws_lambda.Runtime('python3.8'),
            environment={
                'DYNAMODB_TABLE': table and table.table_name,
                'QUEUE_URL': queue and queue.queue_url
            },
        )
        if table is not None:
            table.grant_read_write_data(lambda_function)
        if queue is not None:
            queue.grant_send_messages(lambda_function)
            lambda_function.add_event_source(
                event_sources.SqsEventSource()
            )
        if bucket is not None:
            bucket.grant_read_write(lambda_function)
            lambda_function.add_event_source(
                event_sources.S3EventSource(bucket=bucket, events=[s3.EventType.OBJECT_CREATED])
            )

        return lambda_function




