from datetime import datetime, timedelta
from app.interfaces.payclub_interface import IPayclubService, IPayclubRepository
from app.decorators.payclub_token_provider import payclub_token_provider
from app.utils.parse_datetime_to_string import parse_datetime_to_payclub_date_format


class PayclubService(IPayclubService):

    def __init__(self, repository: IPayclubRepository):
        self.repository = repository

    def get_authorization_token(self):
        response = self.repository.get_authorization_response()
        json_response = response.json()
        access_token = json_response.get("access_token", None)
        expiration_time = json_response.get("expires_in", None)
        return access_token, expiration_time

    @payclub_token_provider
    def get_last_24_hours_transactions(self, access_token: str):
        today = datetime.now()
        yesterday = today - timedelta(hours=24)

        date_from = parse_datetime_to_payclub_date_format(yesterday)
        date_to = parse_datetime_to_payclub_date_format(today)
        response = self.repository.get_credits_transactions_by_date(
            access_token, date_from, date_to)
        transactions_history = response.json().get('data', [])
        return transactions_history

    @payclub_token_provider
    def get_transactions_by_date(self, access_token, date_from, date_to):
        response = self.repository.get_credits_transactions_by_date(
            access_token, date_from, date_to)
        transactions_history = response.json().get('data', [])
        return transactions_history
