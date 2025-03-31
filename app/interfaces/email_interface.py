from abc import ABC, abstractmethod


class IEmailService(ABC):
    @abstractmethod
    def get_or_create_instance():
        pass

    @abstractmethod
    def send_email(self, to_email, b64_pdf):
        pass
