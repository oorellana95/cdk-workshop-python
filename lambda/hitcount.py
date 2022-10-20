import json
import os

import boto3

# You’ll notice that this code relies on two environment variables:
# HITS_TABLE_NAME is the name of the DynamoDB table to use for storage.
# DOWNSTREAM_FUNCTION_NAME is the name of the downstream AWS Lambda function.

# Since the actual name of the table and the downstream function will only be decided when we deploy our app,
# we need to wire up these values from our construct code. We’ll do that in the next section.

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["HITS_TABLE_NAME"])
_lambda = boto3.client("lambda")


def handler(event, context):
    print("request: {}".format(json.dumps(event)))
    table.update_item(
        Key={"path": event["path"]},
        UpdateExpression="ADD hits :incr",
        ExpressionAttributeValues={":incr": 1},
    )

    resp = _lambda.invoke(
        FunctionName=os.environ["DOWNSTREAM_FUNCTION_NAME"], Payload=json.dumps(event)
    )

    body = resp["Payload"].read()

    print("downstream response: {}".format(body))
    return json.loads(body)
