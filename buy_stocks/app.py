import requests
import boto3
import os
# from opentelemetry import trace


def lambda_handler(event, context):
    if 'AWS_SAM_LOCAL' in os.environ:
        s3 = boto3.client('s3', endpoint_url="http://host.docker.internal:4566")
    else:
        s3 = boto3.client('s3')
    alpaca_id = os.environ['ALPACA_ID']
    alpaca_secret = os.environ['ALPACA_SECRET']
    headers = {'APCA-API-KEY-ID': alpaca_id, 'APCA-API-SECRET-KEY': alpaca_secret}

    rankings_file = s3.get_object(Bucket=os.environ['BUCKET_NAME'], Key='rankings.txt')
    # stock_ranking = rankings_file['Body'].read().decode('utf-8').split(' ')

    # customizedSpan = trace.get_current_span()
    # customizedSpan.set_attribute("alpaca.id", alpaca_id);
    # customizedSpan.set_attribute("alpaca.secret", alpaca_secret);
    # customizedSpan.set_attribute("rankings", str(stock_ranking));

    for i in range(3):
        buy_response = requests.post('https://paper-api.alpaca.markets/v2/orders', headers=headers,
                                     json={'symbol': stock_ranking[i], 'qty': 1, 'side': 'buy', 'type': 'market',
                                           'time_in_force': 'day'})

    return {
        'statusCode': 200,
        'body': requests.get('https://paper-api.alpaca.markets/v2/positions', headers=headers).json()
    }
