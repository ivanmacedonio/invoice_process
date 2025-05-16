from datetime import datetime, timedelta
from app.domain.interfaces.Mercadopago_interface import IMercadopagoService, IMercadopagoRepository
from app.domain.decorators.Mercadopago_token_provider import Mercadopago_token_provider
from app.domain.utils.parse_datetime_to_string import parse_datetime_to_Mercadopago_date_format


class MercadopagoService(IMercadopagoService):

    def __init__(self, repository: IMercadopagoRepository):
        self.repository = repository

    def get_authorization_token(self):
        response = self.repository.get_authorization_response()
        json_response = response.json()
        access_token = json_response.get("access_token", None)
        expiration_time = json_response.get("expires_in", None)
        return access_token, expiration_time

    @Mercadopago_token_provider
    def get_last_24_hours_transactions(self, access_token: str):
        today = datetime.now()
        yesterday = today - timedelta(hours=24)

        date_from = parse_datetime_to_Mercadopago_date_format(yesterday)
        date_to = parse_datetime_to_Mercadopago_date_format(today)
        response = self.repository.get_credits_transactions_by_date(
            access_token, date_from, date_to)
        return response

    @Mercadopago_token_provider
    def get_transactions_by_date(self, access_token, date_from, date_to):
        response = self.repository.get_credits_transactions_by_date(
            access_token, date_from, date_to)
        return response
