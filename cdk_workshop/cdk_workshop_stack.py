from constructs import Construct
from aws_cdk import (
    Stack,
    # We are importing the aws_lambda module as _lambda because lambda is a built-in identifier in Python.
    aws_lambda as _lambda,
    aws_apigateway as apigw
)

from cdk_workshop.hitcounter import HitCounter
from cdk_dynamo_table_view import TableViewer


class CdkWorkshopStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        my_lambda = _lambda.Function(
            self,
            'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_9,
            # The handler code is loaded from the lambda directory which we created earlier.
            # Path is relative to where you execute cdk from, which is the project’s root directory
            code=_lambda.Code.from_asset('lambda'),
            # The name of the handler function is hello.handler (“hello” is the name of the file and “handler”
            # is the function name)
            handler='hello.handler'
        )

        hello_with_counter = HitCounter(
            self, 'HelloHitCounter',
            downstream=my_lambda,
        )

        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=hello_with_counter.handler,
        )

        TableViewer(
            self, 'ViewHitCounter',
            title='Hello Hits',
            table=hello_with_counter.table,
            sort_by='-hits'
        )
