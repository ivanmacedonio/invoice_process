from abc import ABC, abstractmethod


class ITokenManager:
    @abstractmethod
    def __init__(self, Mercadopago_service):
        if not Mercadopago_service:
            raise ValueError('Mercadopago_service arg is missing')
        pass

    @abstractmethod
    def get_token(self):
        pass
