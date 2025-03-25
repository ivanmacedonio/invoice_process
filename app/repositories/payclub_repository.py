import requests
from app.configs.environments import PVS_BASE_URL_PATH, PVS_CLIENT_ID, PVS_CLIENT_SECRET, PVS_APP_NAME
from requests.auth import HTTPBasicAuth
from app.configs.logger import logger
from app.interfaces.payclub_interface import IPayclubRepository
from app.entities.dataclasses.payclub_payload_dataclass import PayclubAuthQueryPayload, PayclubQueryPayload


class PayclubRequestException(requests.RequestException):

    def __init__(self, response):
        super().__init__(response)
        self.response = response
        self.status_code = response.status_code

    def get_error_message(self):
        try:
            logger.error(f'Payclub error response: {self.response.text}')
            return self.response.json().get("error", {}).get("serviceErrorMessage", "No error message provided")
        except ValueError:
            return "No error message provided"

    def __str__(self):
        return f'status_code: {self.status_code} - error_message: {self.get_error_message()}'


class PayclubRepository(IPayclubRepository):

    def __init__(self):
        pass

    def get_authorization_response(self):
        query_payload = PayclubAuthQueryPayload(**{
            "url": f'{PVS_BASE_URL_PATH}/platformx/auth/token',
            "username": PVS_CLIENT_ID,
            "password": PVS_CLIENT_SECRET,
            "body": {
                "grant_type": "client_credentials",
                "scope": "simplescope"
            },
            "headers":  {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })

        authentication_method = HTTPBasicAuth(
            username=query_payload.username, password=query_payload.password)

        response = requests.post(
            url=query_payload.url, headers=query_payload.headers, auth=authentication_method, data=query_payload.body)

        logger.info(
            f'Payclub token retrieve response status code: {str(response.status_code)}')

        if response.status_code > 299:
            raise PayclubRequestException(response)

        return response

    def get_credits_transactions_by_date(self, access_token, date_from, date_to):
        query_params = f'dateTimeFrom={date_from}&dateTimeTo={date_to}'
        query_payload = PayclubQueryPayload(**{
            'url': f'{PVS_BASE_URL_PATH}/pxadapters/hlpoints/company/SC000001?{query_params}',
            'headers': {'Authorization': f'Bearer {access_token}', 'appname': PVS_APP_NAME}
        })
        response = requests.get(url=query_payload.url,
                                headers=query_payload.headers)

        if response.status_code > 299:
            raise PayclubRequestException(response)

        logger.info(
            f'Iterating over {response.json().get('pagination', {}).get('total_records', None)} transactions')

        return response
