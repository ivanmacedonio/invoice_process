from functools import wraps
import time
from repositories.payclub_repository import PayclubRepository
from interfaces.payclub_interface import IPayclubRepository
from configs.environments import PVS_BASE_URL_PATH, PVS_CLIENT_ID, PVS_CLIENT_SECRET
from configs.logger import logger

token_manager_instance = None


class TokenManager:

    def __init__(self):

        self._cached_token = None
        self._token_expiration = 0
        logger.info("creando instancia de TOKEN")

    def get_token(self, query_payload: dict, payclub_repository: IPayclubRepository):

        if self._cached_token and time.time() < self._token_expiration:
            return self._cached_token

        json_response = payclub_repository.get_authorization_response(
            query_payload)

        self._cached_token = json_response.get("access_token", None)

        if not self._cached_token:
            logger.error(
                f'invalid value for _cached_token variable: {self._cached_token}')

        _expires_in_time_in_seconds: int = int(
            json_response.get("expires_in"))

        if not self._cached_token:
            raise KeyError("access_token attribute is missing in response")

        self._token_expiration = time.time() + _expires_in_time_in_seconds

        return self._cached_token


def token_manager_singleton():
    global token_manager_instance
    if not token_manager_instance:
        payclub_repository = PayclubRepository()
        token_manager_instance = TokenManager(payclub_repository)
    return token_manager_instance


def payclub_token_provider(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        query_payload: dict = {
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
        }
        token_manager = token_manager_singleton()
        access_token = token_manager.get_token(query_payload)
        return func(*args, access_token=access_token, **kwargs)

    return wrapper
