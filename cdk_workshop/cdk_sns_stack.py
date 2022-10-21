import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_sns as sns,
    aws_logs as logs,
)

from constructs import Construct


class CdkSnsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create SNS Topic
        topic = sns.Topic(self, 'sns-to-lambda-topic', display_name='My SNS topic')
        lambda_function = _lambda.Function(
            self,
            "SNSPublisher",
            runtime=_lambda.Runtime.PYTHON_3_9,
            # The handler code is loaded from the lambda directory which we created earlier.
            # Path is relative to where you execute cdk from, which is the project’s root directory
            code=_lambda.Code.from_asset("lambda"),
            # The name of the handler function is hello.handler (“hello” is the name of the file and “handler”
            # is the function name)
            handler="parent.handler",
            timeout=cdk.Duration.seconds(10)
        )

        # Set Lambda Logs Retention and Removal Policy
        logs.LogGroup(
            self,
            'logs',
            log_group_name=f"/aws/lambda/{lambda_function.function_name}",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            retention=logs.RetentionDays.ONE_DAY
        )

        # Grant publish to lambda function
        topic.grant_publish(lambda_function)

        cdk.CfnOutput(self,
                      'snsTopicArn',
                      value=topic.topic_arn,
                      description='The arn of the SNS topic')

        cdk.CfnOutput(self,
                      'functionName',
                      value=lambda_function.function_name,
                      description='The name of the handle function')
