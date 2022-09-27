import json
import requests
import boto3
import os


# from opentelemetry import trace

def lambda_handler(event, context):
    if 'AWS_SAM_LOCAL' in os.environ:
        print('local')
        s3 = boto3.resource('s3', endpoint_url="http://host.docker.internal:4566")
    else:
        print('Not Local')
        s3 = boto3.resource('s3')

    alpaca_id = os.environ['ALPACA_ID']
    alpaca_secret = os.environ['ALPACA_SECRET']
    headers = {'APCA-API-KEY-ID': alpaca_id, 'APCA-API-SECRET-KEY': alpaca_secret}
    symbols = []

    wl_response = requests.get('https://paper-api.alpaca.markets/v2/watchlists', headers=headers)
    wl_id = wl_response.json()[0].get('id')
    watchlist_response = requests.get('https://paper-api.alpaca.markets/v2/watchlists/' + wl_id, headers=headers)
    for entity in watchlist_response.json().get('assets'):
        symbols.append(entity.get('symbol'))
    encoded_string = ' '.join(symbols).encode('utf-8')

    s3.Bucket(os.environ['BUCKET_NAME']).put_object(Key='watchlist.txt', Body=encoded_string)

    return {
        'statusCode': 200,
        'body': json.dumps(encoded_string.decode('utf-8'))
    }
