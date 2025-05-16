from unittest.mock import MagicMock, patch
from unittest import TestCase

with patch('app.domain.decorators.Mercadopago_token_provider.Mercadopago_token_provider', lambda x: x):
    from app.domain.services.wallet import MercadopagoService


class MercadopagoServiceTest(TestCase):

    @classmethod
    def setup_repository(self):
        self.Mercadopago_repository = MagicMock()

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
            {"product": "Mercadopago_transaction"}
        ]
        return dummy_response

    @classmethod
    def setup_Mercadopago_service(self):
        self.Mercadopago_service = MercadopagoService(self.Mercadopago_repository)

    @classmethod
    def setUp(self):
        self.setup_repository()
        self.setup_Mercadopago_service()

    def test_get_authorization_token_works_successfully(self):
        dummy_response = self.get_authorization_response()
        self.Mercadopago_repository.get_authorization_response.return_value = dummy_response

        access_token, expiration_time = self.Mercadopago_service.get_authorization_token()

        self.assertEqual(access_token, "dummy_token")
        self.assertEqual(expiration_time, 3000)

    def test_get_transactions_by_date(self):
        dummy_response = self.get_transactions_response()
        self.Mercadopago_repository.get_credits_transactions_by_date.return_value = dummy_response
        transactions_history = self.Mercadopago_service.get_transactions_by_date(
            "dummy_token", "test_date_from", "test_date_to")

        self.assertTrue(len(transactions_history), 1)
        self.assertEqual(
            transactions_history[0]['product'], "Mercadopago_transaction")
