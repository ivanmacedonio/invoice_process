from abc import ABC, abstractmethod


class ITokenManager:
    @abstractmethod
    def __init__(self, payclub_service):
        if not payclub_service:
            raise ValueError('payclub_service arg is missing')
        pass

    @abstractmethod
    def get_token(self):
        pass
