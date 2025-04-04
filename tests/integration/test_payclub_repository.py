from unittest import TestCase
from unittest.mock import MagicMock
from app.repositories.payclub_repository import PayclubRepository, PayclubRequestException
from app.interfaces.payclub_interface import IPayclubRepository


class TestPayclubRepository(TestCase):

    def setUpDummyDatesRange(self):
        self.date_from = "20250301 00:00:00"
        self.date_to = "20250310 23:59:59"

    def setUpRepository(self):
        payclub_repository: IPayclubRepository = PayclubRepository()
        self.repository = payclub_repository

    def setUp(self):
        self.setUpRepository()
        self.setUpDummyDatesRange()

    def test_authorization_payclub_endpoint(self):
        response = self.repository.get_authorization_response()
        self.assertTrue(hasattr(response, 'json'))

        json_response = response.json()
        self.assertIsNotNone(json_response.get('access_token', None))
        self.assertIsNotNone(json_response.get('expires_in', None))
        self.assertEqual(json_response.get('token_type'), 'Bearer')
        self.assertIsInstance(json_response.get('access_token'), str)

    def test_get_transactions_endpoint_with_custom_dates(self):
        authorization_response = self.repository.get_authorization_response()
        access_token = authorization_response.json().get('access_token', None)
        get_transactions_response = self.repository.get_credits_transactions_by_date(
            access_token, self.date_from, self.date_to)

        json_response = get_transactions_response
        self.assertIsNotNone(access_token)
        self.assertIsInstance(json_response, list)
        self.assertGreater(len(json_response), 0)

    def test_custom_exception_raises_successfully(self):
        dummy_response = MagicMock()
        dummy_response.json.return_value = {
            "error": {
                "serviceErrorMessage": "dummy_error"
            }
        }
        dummy_response.status_code = 400
        with self.assertRaises(PayclubRequestException) as context:
            raise PayclubRequestException(dummy_response)

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(str(context.exception),
                         "status_code: 400 - error_message: dummy_error")
