echo "Removing resources..."

echo "Removing DynamoDB Table..."
cd resources/dynamodb && serverless remove
echo "Removing SQS queues..."
cd ../../resources/sqs && serverless remove

echo "Resources deleted successfully"

echo "Removing services"
cd ../../services/crud_dynamodb && serverless remove
cd ../../services/s3_sqs && serverless remove
cd ../../services/sqs_dynamodb && serverless remove
