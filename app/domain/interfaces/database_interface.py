from abc import ABC, abstractmethod


class IDatabase(ABC):
    def __new__(cls, *args, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def create_connection_string():
        pass

    @abstractmethod
    def get_or_create_db(self):
        pass

    @abstractmethod
    def get_local_session(self):
        pass
