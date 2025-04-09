from abc import ABC, abstractmethod


class IDiscord(ABC):

    @abstractmethod
    def parse_message(self, content):
        pass

    @abstractmethod
    def execute_webhook(self):
        pass
