echo "Creating resources..."


echo "Creating DynamoDB Table..."
cd resources/dynamodb && serverless deploy
echo "Creating SQS queues..."
cd ../../resources/sqs && serverless deploy

echo "Resources created successfully"

echo "Creating services"

cd ../../services/crud_dynamodb && serverless deploy
cd ../../services/s3_sqs && serverless deploy
cd ../../services/sqs_dynamodb && serverless deploy
