import time
from configs.logger import logger


class TokenManager:

    def __init__(self, payclub_service):
        self._cached_token = None
        self._token_expiration = 0
        self.payclub_service = payclub_service

    def get_token(self):
        if self._cached_token and time.time() < self._token_expiration:
            return self._cached_token

        access_token, _expires_in_time_in_seconds = self.payclub_service.get_authorization_token()

        self._cached_token = access_token

        if not self._cached_token:
            logger.error(
                f'invalid value for _cached_token variable: {self._cached_token}')

        if not self._cached_token:
            raise KeyError("access_token attribute is missing in response")

        self._token_expiration = time.time() + _expires_in_time_in_seconds

        return self._cached_token
