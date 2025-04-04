from unittest.mock import MagicMock, patch
from unittest import TestCase

with patch('app.decorators.payclub_token_provider.payclub_token_provider', lambda x: x):
    from app.services.payclub import PayclubService


class PayclubServiceTest(TestCase):

    @classmethod
    def setup_repository(self):
        self.payclub_repository = MagicMock()

    @classmethod
    def get_authorization_response(self):
        dummy_response = MagicMock()
        dummy_response.json.return_value = {
            "access_token": "dummy_token",
            "expires_in": 3000
        }
        return dummy_response

    @classmethod
    def get_transactions_response(self):
        dummy_response = MagicMock()
        dummy_response = [
            {"product": "payclub_transaction"}
        ]
        return dummy_response

    @classmethod
    def setup_payclub_service(self):
        self.payclub_service = PayclubService(self.payclub_repository)

    @classmethod
    def setUp(self):
        self.setup_repository()
        self.setup_payclub_service()

    def test_get_authorization_token_works_successfully(self):
        dummy_response = self.get_authorization_response()
        self.payclub_repository.get_authorization_response.return_value = dummy_response

        access_token, expiration_time = self.payclub_service.get_authorization_token()

        self.assertEqual(access_token, "dummy_token")
        self.assertEqual(expiration_time, 3000)

    def test_get_transactions_by_date(self):
        dummy_response = self.get_transactions_response()
        self.payclub_repository.get_credits_transactions_by_date.return_value = dummy_response
        transactions_history = self.payclub_service.get_transactions_by_date(
            "dummy_token", "test_date_from", "test_date_to")

        self.assertTrue(len(transactions_history), 1)
        self.assertEqual(
            transactions_history[0]['product'], "payclub_transaction")
