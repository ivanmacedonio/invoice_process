import time
from unittest.mock import patch, MagicMock
from unittest import TestCase
from app.services.token_manager import TokenManager


class TestTokenManager(TestCase):

    @classmethod
    def setup_mocked_payclub_service(self):
        self.mocked_payclub_service = MagicMock()
        self.mocked_payclub_service.get_authorization_token.return_value = "dummy_token", 3000

    @classmethod
    def setup_token_manager(self):
        token_manager = TokenManager(self.mocked_payclub_service)
        self.token_manager = token_manager

    @classmethod
    def setUp(self):
        self.setup_mocked_payclub_service()
        self.setup_token_manager()

    def test_token_is_stored_successfully(self):
        token = self.token_manager.get_token()

        self.assertIsNotNone(token)

    def test_get_token_when_cached_token_is_expired(self):
        self.token_manager._cached_token = 'expired_token'
        self.token_manager._token_expiration = time.time() - 60

        self.mocked_payclub_service.get_authorization_token.return_value = (
            'new_token', 3600)

        result = self.token_manager.get_token()

        self.assertEqual(result, 'new_token')
        self.mocked_payclub_service.get_authorization_token.assert_called_once()
