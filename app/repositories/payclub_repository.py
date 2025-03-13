import requests
from requests.auth import HTTPBasicAuth
from configs.logger import logger
from configs.environments import PVS_BASE_URL_PATH
from interfaces.payclub_interface import IPayclubRepository


class PayclubRepository(IPayclubRepository):

    def __init__(self):
        pass

    def get_authorization_response(self, query_payload: dict):

        if not query_payload['username'] or not query_payload['password']:
            raise TypeError("Invalid PVS username or password")

        authentication_method = HTTPBasicAuth(
            username=query_payload['username'], password=query_payload['password'])

        response = requests.post(
            url=query_payload['url'], headers=query_payload['headers'], auth=authentication_method, data=query_payload['body'])

        if response.status_code > 299:
            logger.error(f'Failed PVS response: {str(response)}')
            raise requests.RequestException(
                "Error while trying to fetch PVS auth token")

        return response.json()

    def get_credits_transactions(self, query_payload: dict):

        pass
