from functools import wraps
from app.domain.interfaces.payclub_interface import IPayclubRepository, IPayclubService

token_manager_instance = None


def token_manager_singleton():
    global token_manager_instance
    if not token_manager_instance:
        from app.domain.services.token_manager import TokenManager
        from app.adapters.outbound.repositories.payclub_repository import PayclubRepository
        from app.domain.services.wallet import PayclubService

        payclub_repository: IPayclubRepository = PayclubRepository()
        payclub_service: IPayclubService = PayclubService(payclub_repository)
        token_manager_instance = TokenManager(payclub_service)
    return token_manager_instance


def payclub_token_provider(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        token_manager = token_manager_singleton()
        access_token = token_manager.get_token()
        return func(*args, access_token=access_token, **kwargs)

    return wrapper
