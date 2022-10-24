import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_dynamodb as ddb
)

from constructs import Construct


class CdkSECStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        _table = ddb.Table(
            self,
            "sec_company_facts",
            partition_key={"name": "ticker", "type": ddb.AttributeType.STRING}
        )

        _lambda_retrieve_company_tickers_exchange = _lambda.Function(self, "SECRetrieveCompanyTickersExchangeLambda",
                                                                     code=_lambda.Code.from_asset(
                                                                         "lambda",
                                                                         bundling=cdk.BundlingOptions(
                                                                             image=_lambda.Runtime.PYTHON_3_9.bundling_image,
                                                                             command=['bash', '-c',
                                                                                      'pip install pandas'],
                                                                         )),
                                                                     runtime=_lambda.Runtime.PYTHON_3_9,
                                                                     handler="sec.retrieve_company_tickers_exchange.handler",
                                                                     timeout=cdk.Duration.seconds(25))

        _lambda_upgrade_in_dynamodb_company_facts = _lambda.Function(self,
                                                                     "SECUpgradeInDynamoDbCompanyFactsLambda",
                                                                     code=_lambda.Code.from_asset(
                                                                         "lambda",
                                                                         bundling=cdk.BundlingOptions(
                                                                             image=_lambda.Runtime.PYTHON_3_9.bundling_image,
                                                                             command=['bash', '-c',
                                                                                      'pip install boto3'],
                                                                         )),
                                                                     runtime=_lambda.Runtime.PYTHON_3_9,
                                                                     handler="sec.upgrade_in_dynamodb_company_facts.handler",
                                                                     environment={
                                                                         "SEC_TABLE_NAME": _table.table_name,
                                                                     })

        sfn.StateMachine(self,
                         "ApplicationStateMachine",
                         definition=sfn.Chain.start(
                             tasks.LambdaInvoke(self,
                                                "RetrieveCompanyTickersExchangeTask",
                                                lambda_function=_lambda_retrieve_company_tickers_exchange,
                                                payload_response_only=True,
                                                result_path='$.list_company_tickers_exchange')
                         ).next(
                             sfn.Map(self,
                                     'UpgradeMultipleMapState',
                                     input_path='$.company_ticker_exchange',
                                     items_path='$.list_company_tickers_exchange',
                                     max_concurrency=1000)
                             .iterator(
                                 tasks.LambdaInvoke(self,
                                                    "UpgradeInDynamoDbCompanyFacts",
                                                    lambda_function=_lambda_upgrade_in_dynamodb_company_facts,
                                                    payload_response_only=True)
                             )
                         ))
