import pandas as pd


def handler(event, context):
    """Retrieve company tickers exchange from the api SEC and returns a list of dictionaries with cik, name, ticker and
    exchange as a response: [{'cik': 320193, 'name': 'Apple Inc.', 'ticker': 'AAPL', 'exchange': 'Nasdaq'}, ...]"""
    # TODO Manage exceptions
    api_hardcoded = {'fields': ['cik', 'name', 'ticker', 'exchange'],
                     'data': [[320193, 'Apple Inc.', 'AAPL', 'Nasdaq'],
                              [789019, 'MICROSOFT CORP', 'MSFT', 'Nasdaq'],
                              [1067983, 'BERKSHIRE HATHAWAY INC', 'BRK-B', 'NYSE'],
                              [731766, 'UNITEDHEALTH GROUP INC', 'UNH', 'NYSE']]}
    df = pd.DataFrame(data=api_hardcoded.get('data'), columns=api_hardcoded.get('fields'))
    return df.to_dict(orient='records')
