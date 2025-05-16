from functools import wraps
from app.domain.interfaces.Mercadopago_interface import IMercadopagoRepository, IMercadopagoService

token_manager_instance = None


def token_manager_singleton():
    global token_manager_instance
    if not token_manager_instance:
        from app.domain.services.token_manager import TokenManager
        from app.adapters.outbound.repositories.Mercadopago_repository import MercadopagoRepository
        from app.domain.services.wallet import MercadopagoService

        Mercadopago_repository: IMercadopagoRepository = MercadopagoRepository()
        Mercadopago_service: IMercadopagoService = MercadopagoService(Mercadopago_repository)
        token_manager_instance = TokenManager(Mercadopago_service)
    return token_manager_instance


def Mercadopago_token_provider(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        token_manager = token_manager_singleton()
        access_token = token_manager.get_token()
        return func(*args, access_token=access_token, **kwargs)

    return wrapper
