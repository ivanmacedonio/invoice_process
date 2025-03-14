from abc import abstractmethod, ABC


class IPayclubService(ABC):

    @abstractmethod
    def __init__(self, repository):
        pass

    @abstractmethod
    def get_authorization_token(self):
        pass

    @abstractmethod
    def get_last_24_hours_transactions(self, access_token):
        pass


class IPayclubRepository(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_authorization_response(self):
        pass

    @abstractmethod
    def get_credits_transactions_by_date(self, access_token, date_from, date_to):
        if not all([access_token, date_from, date_to]):
            raise ValueError("missing fields while trying to get transactions history")
        pass