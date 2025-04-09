from abc import ABC, abstractmethod


class IDiscord(ABC):

    @abstractmethod
    def parse_message(self, content):
        pass

    @abstractmethod
    def execute_webhook(self):
        pass


class ICounterManager(ABC):

    @abstractmethod
    def push_approved(cls, v: int):
        pass

    @abstractmethod
    def push_total(cls, v: int):
        pass

    @abstractmethod
    def push_money_amount(cls, v: int):
        pass

    @abstractmethod
    def get_amounts(self):
        pass
