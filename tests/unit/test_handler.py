import json
import pytest
from watchlist_updater import app


class TestClass:

    @pytest.fixture()
    def apigw_event(self):
        """ Generates API GW Event"""
        return {
            "body": '{ "test": "body"}',
            "resource": "/{proxy+}",
            "requestContext": {
                "resourceId": "123456",
                "apiId": "1234567890",
                "resourcePath": "/{proxy+}",
                "httpMethod": "POST",
                "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
                "accountId": "123456789012",
                "identity": {
                    "apiKey": "",
                    "userArn": "",
                    "cognitoAuthenticationType": "",
                    "caller": "",
                    "userAgent": "Custom User Agent String",
                    "user": "",
                    "cognitoIdentityPoolId": "",
                    "cognitoIdentityId": "",
                    "cognitoAuthenticationProvider": "",
                    "sourceIp": "127.0.0.1",
                    "accountId": "",
                },
                "stage": "prod",
            },
            "queryStringParameters": {"foo": "bar"},
            "headers": {
                "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
                "Accept-Language": "en-US,en;q=0.8",
                "CloudFront-Is-Desktop-Viewer": "true",
                "CloudFront-Is-SmartTV-Viewer": "false",
                "CloudFront-Is-Mobile-Viewer": "false",
                "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
                "CloudFront-Viewer-Country": "US",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Upgrade-Insecure-Requests": "1",
                "X-Forwarded-Port": "443",
                "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
                "X-Forwarded-Proto": "https",
                "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
                "CloudFront-Is-Tablet-Viewer": "false",
                "Cache-Control": "max-age=0",
                "User-Agent": "Custom User Agent String",
                "CloudFront-Forwarded-Proto": "https",
                "Accept-Encoding": "gzip, deflate, sdch",
            },
            "pathParameters": {"proxy": "/examplepath"},
            "httpMethod": "POST",
            "stageVariables": {"baz": "qux"},
            "path": "/examplepath",
        }

    @pytest.fixture()
    def mock_env_alpaca_id(self, monkeypatch):
        monkeypatch.setenv("ALPACA_ID", "Foo")

    @pytest.fixture()
    def mock_env_alpaca_secret(self, monkeypatch):
        monkeypatch.setenv("ALPACA_SECRET", "Bar")

    # @pytest.fixture()
    # def alpaca_api_call_one(self):
    #     with requests_mock.Mocker() as mock:
    #         mock.get(
    #             'https://paper-api.alpaca.markets/v2/watchlists',
    #             json={"id": "123"})

    def test(self, apigw_event, monkeypatch):
        monkeypatch.setenv("ALPACA_ID", "Foo")
        monkeypatch.setenv("ALPACA_SECRET", "Bar")
        handler_result = app.lambda_handler(apigw_event, "")
        data = json.loads(handler_result["body"])
        assert handler_result["statusCode"] == 200
