import requests
from app.config.dependencies import MP_BASE_URL_PATH, MP_CLIENT_ID, MP_CLIENT_SECRET, MP_APP_NAME, MP_BODY, MP_HEADERS
from requests.auth import HTTPBasicAuth
from app.config.logger import logger
from app.domain.interfaces.Mercadopago_interface import IMercadopagoRepository
from app.domain.entities.dataclasses.Mercadopago_payload_dataclass import MercadopagoAuthQueryPayload, MercadopagoQueryPayload


class MercadopagoRequestException(requests.RequestException):

    def __init__(self, response):
        super().__init__(response)
        self.response = response
        self.status_code = response.status_code

    def get_error_message(self):
        try:
            logger.error(f'Mercadopago error response: {self.response.text}')
            return self.response.json().get("error", {}).get("serviceErrorMessage", "No error message provided")
        except ValueError:
            return "No error message provided"

    def __str__(self):
        return f'status_code: {self.status_code} - error_message: {self.get_error_message()}'


class MercadopagoRepository(IMercadopagoRepository):

    def __init__(self):
        self.page = 1
        self.pages_amount = 1

    def get_authorization_response(self):
        query_payload = MercadopagoAuthQueryPayload(**{
            "url": f'{MP_BASE_URL_PATH}/authorization',
            "username": MP_CLIENT_ID,
            "password": MP_CLIENT_SECRET,
            "body": MP_BODY,
            "headers": MP_HEADERS
        })

        authentication_method = HTTPBasicAuth(
            username=query_payload.username, password=query_payload.password)

        response = requests.post(
            url=query_payload.url, headers=query_payload.headers, auth=authentication_method, data=query_payload.body)

        logger.info(
            f'Mercadopago token retrieve response status code: {str(response.status_code)}')

        if response.status_code > 299:
            raise MercadopagoRequestException(response)

        return response

    def get_credits_transactions_by_date(self, access_token, date_from, date_to):
        if self.page > self.pages_amount:
            return []  # break the callback if is out of index

        query_params = f'dateTimeFrom={date_from}&dateTimeTo={date_to}&page={self.page}&per_page={50}'
        query_payload = MercadopagoQueryPayload(**{
            'url': f'{MP_BASE_URL_PATH}/pxadapters/hlpoints/company/SC000001?{query_params}',
            'headers': {'Authorization': f'Bearer {access_token}', 'appname': MP_APP_NAME}
        })
        response = requests.get(url=query_payload.url,
                                headers=query_payload.headers)

        if response.status_code > 299:
            raise MercadopagoRequestException(response)

        pagination_data = response.json().get('pagination', {})
        self.pages_amount = pagination_data.get('total_pages')

        logger.info(
            f'Page {self.page}/{pagination_data.get('total_pages')}'
        )
        logger.info(
            f'Iterating over {len(response.json().get('data', []))} transactions')

        self.page = self.page + 1

        return response.json().get('data')
