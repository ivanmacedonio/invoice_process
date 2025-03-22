from abc import abstractmethod, ABC


class IBillingService(ABC):
    @abstractmethod
    def __init__(self, instance_manager, builder_manager, repository):
        if not all([instance_manager, builder_manager, repository]):
            raise ValueError(
                'lack of arguments while trying to instance BillingService')
        pass

    @abstractmethod
    def bill(self, transaction):
        if not transaction:
            raise ValueError('transaction arg is missing')
        pass


class IInstanceManager(ABC):
    @abstractmethod
    def get_or_create_instance(self, invoicer_data):
        if not invoicer_data:
            raise ValueError('invoicer_data arg is missing')
        pass


class IBuildManager(ABC):
    @abstractmethod
    def build_invoice(self, transaction, invoicer_data, arca_instance):
        pass
