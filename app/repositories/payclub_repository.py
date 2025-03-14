import requests
from requests.auth import HTTPBasicAuth
from configs.logger import logger
from configs.environments import PVS_BASE_URL_PATH
from interfaces.payclub_interface import IPayclubRepository
from entities.query_payload import PayclubAuthQueryPayload


class PayclubRepository(IPayclubRepository):

    def __init__(self):
        pass

    def get_authorization_response(self, query_payload: PayclubAuthQueryPayload):

        authentication_method = HTTPBasicAuth(
            username=query_payload.username, password=query_payload.password)

        response = requests.post(
            url=query_payload.url, headers=query_payload.headers, auth=authentication_method, data=query_payload.body)

        logger.info(f'Payclub token retrieve response: {str(response)}')

        if response.status_code > 299:
            raise requests.RequestException(
               f'Error while trying to fetch PVS auth token: {str(response)}')

        return response.json()

    def get_credits_transactions(self, query_payload: dict):

        pass
