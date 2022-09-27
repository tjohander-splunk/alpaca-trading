import json
import requests
import os
# from opentelemetry import trace


def lambda_handler(event, context):
    ticker = event['symbol']
    finnhub_token = os.environ['FINNHUB_TOKEN']

    # customizedSpan = trace.get_current_span()
    # customizedSpan.set_attribute("symbol", ticker);
    # customizedSpan.set_attribute("finnhub.token", finnhub_token);

    output = {}
    output['ticker'] = ticker

    quote = requests.get(f'https://finnhub.io/api/v1/quote?symbol={ticker}&token={finnhub_token}')
    quote_json = json.loads(
        str(quote.json()).replace('\'', '"').replace('None', '"None"').replace('True', '"True"').replace('False',
                                                                                                         '"False"'))
    output['quote'] = quote_json

    return output
