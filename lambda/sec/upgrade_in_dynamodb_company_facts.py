from botocore.exceptions import ClientError
import os
import boto3

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["SEC_TABLE_NAME"])


def handler(event, context):
    company_ticker_exchange = event.get("company_ticker_exchange")
    ticker = company_ticker_exchange.get("ticker")
    concepts = [
        {
            "concept_name": "SalesTypeLeaseNetInvestmentInLeaseAfterAllowanceForCreditLoss",
            "unit_type": "USD",
            "value": 91000000,
            "year": 2020,
            "filed": "2022-02-07",
        },
        {
            "concept_name": "SalesTypeLeaseNetInvestmentInLeaseAfterAllowanceForCreditLoss",
            "unit_type": "USD",
            "value": 376000000,
            "year": 2021,
            "filed": "2022-02-07",
        },
        {
            "concept_name": "SalesTypeLeaseNetInvestmentInLeaseAllowanceForCreditLoss",
            "unit_type": "USD",
            "value": 0,
            "year": 2020,
            "filed": "2022-02-07",
        },
        {
            "concept_name": "SalesTypeLeaseNetInvestmentInLeaseAllowanceForCreditLoss",
            "unit_type": "USD",
            "value": 1000000,
            "year": 2021,
            "filed": "2022-02-07",
        },
        {
            "concept_name": "UndistributedEarningsOfForeignSubsidiaries",
            "unit_type": "USD",
            "value": 161000000,
            "year": 2021,
            "filed": "2022-02-07",
        },
    ]

    try:
        response = table.update_item(
            Key={"ticker": ticker},
            UpdateExpression="SET concepts :c",
            ExpressionAttributeValues={":c": concepts},
            ReturnValues="UPDATED_NEW",
        )
    except ClientError as err:
        print(
            "Couldn't update concepts for %s in table %s. Here's why: %s: %s",
            ticker,
            table.name,
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise
    else:
        return response["Attributes"]
