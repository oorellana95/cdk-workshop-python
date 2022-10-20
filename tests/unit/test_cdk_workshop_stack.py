from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    assertions
)
from cdk_workshop.hitcounter import HitCounter


def test_dynamodb_table_created():
    stack = Stack()
    HitCounter(stack, "HitCounter",
               downstream=_lambda.Function(stack, "TestFunction",
                                           runtime=_lambda.Runtime.PYTHON_3_7,
                                           handler='hello.handler',
                                           code=_lambda.Code.from_asset('lambda')),
               )
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::DynamoDB::Table", 1)


def test_lambda_has_env_vars():
    stack = Stack()
    HitCounter(stack, "HitCounter",
               downstream=_lambda.Function(stack, "TestFunction",
                                           runtime=_lambda.Runtime.PYTHON_3_7,
                                           handler='hello.handler',
                                           code=_lambda.Code.from_asset('lambda')))
    template = assertions.Template.from_stack(stack)
    env_capture = assertions.Capture()
    template.has_resource_properties("AWS::Lambda::Function", {
        "Handler": "hitcount.handler",
        "Environment": env_capture,
    })
    assert env_capture.as_object() == {
        "Variables": {
            "DOWNSTREAM_FUNCTION_NAME": {"Ref": "TestFunction22AD90FC"},
            "HITS_TABLE_NAME": {"Ref": "HitCounterHits079767E5"},
        },
    }


def test_dynamodb_with_encryption():
    stack = Stack()
    HitCounter(stack, "HitCounter",
               downstream=_lambda.Function(stack, "TestFunction",
                                           runtime=_lambda.Runtime.PYTHON_3_7,
                                           handler='hello.handler',
                                           code=_lambda.Code.from_asset('lambda')))

    template = assertions.Template.from_stack(stack)
    template.has_resource_properties("AWS::DynamoDB::Table", {
        "SSESpecification": {
            "SSEEnabled": True,
        },
    })
