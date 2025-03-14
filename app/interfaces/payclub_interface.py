from abc import abstractmethod, ABC


class IPayclubService(ABC):

    @abstractmethod
    def __init__(self):
        pass


class IPayclubRepository(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_authorization_response(self, query_payload):
        if not query_payload:
            raise TypeError('query_payload is required')
        pass
