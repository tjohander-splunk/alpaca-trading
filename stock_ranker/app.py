import json
import pandas as pd
import boto3
import time
import os
# from opentelemetry import trace


def calc_price_change(ticker):
    input_params = {"symbol": ticker}
    if 'AWS_SAM_LOCAL' in os.environ:
        lambda_client = boto3.client('lambda', endpoint_url="http://host.docker.internal:3001")
    else:
        lambda_client = boto3.client('lambda')

    quote = lambda_client.invoke(
        FunctionName=os.environ['GET_FIN_FUNC_NAME'],
        InvocationType='RequestResponse',
        Payload=json.dumps(input_params)
    )
    quote_json = json.load(quote['Payload'])

    close = quote_json.get('quote').get('c')
    prev_close = quote_json.get('quote').get('pc')
    change = round((close / prev_close - 1) * 100, 2)

    return {'ticker': ticker, 'change': change}


def lambda_handler(event, context):
    # While running locally, point clients must point at LocalStack resources
    if 'AWS_SAM_LOCAL' in os.environ:
        print('LOCAL RUN!')
        s3_client = boto3.client('s3', endpoint_url="http://host.docker.internal:4566")
        s3_bucket_resource = boto3.resource('s3', endpoint_url="http://host.docker.internal:4566")
    else:
        s3_client = boto3.client('s3')
        s3_bucket_resource = boto3.resource("s3")

    watchlist_file = s3_client.get_object(Bucket=os.environ['BUCKET_NAME'], Key='watchlist.txt')
    watchlist = watchlist_file['Body'].read().decode('utf-8').split(' ')

    df = pd.DataFrame(columns=['ticker', 'change'])
    for ticker in watchlist:
        df = df.append(calc_price_change(ticker), ignore_index=True)
        time.sleep(1)

    # Build a list of price gains from lowest (loss) to highest (gain)
    df = df.sort_values(by=['change'], ascending=True)
    df = df.reset_index(drop=True)
    stock_ranking = df['ticker'].tolist()

    # customized_span = trace.get_current_span()
    # customized_span.set_attribute("watchlist", str(watchlist))
    # customized_span.set_attribute("rankings", str(stock_ranking))

    # Write the sorted list to S3
    encoded_string = ' '.join(stock_ranking).encode('utf-8')
    s3_bucket_resource.Bucket(os.environ['BUCKET_NAME']).put_object(Key='rankings.txt', Body=encoded_string)

    return {
        'statusCode': 200,
        'body': json.dumps(encoded_string.decode('utf-8'))
    }
