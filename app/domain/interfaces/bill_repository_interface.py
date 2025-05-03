from abc import abstractmethod,  ABC


class IBillRepository(ABC):
    @abstractmethod
    def __init__(self, session):
        if not session:
            raise ValueError(
                'session is required to initializate BillRepository')
        pass

    @abstractmethod
    def get_unique_invoicer(self):
        pass

    @abstractmethod
    def get_or_create_client(self, payload):
        if not payload:
            raise ValueError('payload is required to get or create a client')
        pass

    @abstractmethod
    def create_and_get_sale(self, payload):
        if not payload:
            raise ValueError('payload is required to create a sale')
        pass

    @abstractmethod
    def create_bill(self, bill_payload, client_payload, sell_payload):
        if not all([bill_payload, client_payload, sell_payload]):
            raise ValueError('lack of arguments while trying to create a bill')
        pass

    @abstractmethod
    def close_session(self):
        pass
