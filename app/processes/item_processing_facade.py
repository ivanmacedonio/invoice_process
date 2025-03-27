from app.configs.logger import logger
from afip import Afip
from app.services.database import Database
from app.services.arca import BillingService, BuildManager, InstanceManager
from app.repositories.bill_repository import BillRepository, IBillRepository
from app.builders.bill_builder import BillBuilder
from app.decorators.error_handling_provider import error_handling_provider


class SingletonManager:
    _instances = {}

    @classmethod
    def get_or_create_instance(cls, name: str, create_fn):
        if name not in cls._instances:
            cls._instances[name] = create_fn()
        return cls._instances[name]


def get_or_create_database():
    return SingletonManager.get_or_create_instance('database', lambda: Database())


def get_or_create_repository():
    database: Database = get_or_create_database()
    session = database.create_session()
    return SingletonManager.get_or_create_instance('bill_repository', lambda: BillRepository(session=session))


def get_or_create_arca_instance():
    repository = get_or_create_repository()
    instance_manager = InstanceManager(billing_processor=Afip)
    builder_manager = BuildManager()
    return SingletonManager.get_or_create_instance('arca_instance', lambda: BillingService(instance_manager, builder_manager, repository))


@error_handling_provider
def process_transaction_facade(transaction):
    logger.info(f'Iterating over the follow transaction: {transaction}')

    # setup instances
    arca_instance = get_or_create_arca_instance()
    repository: IBillRepository = get_or_create_repository()

    # billing stuff
    arca_response = arca_instance.bill(transaction)

    # querying stuff
    builded_dtos = BillBuilder().build_dtos(
        transaction=transaction,
        bill_data=arca_response['builded_bill']
    )
    repository.create_bill(
        bill_payload=builded_dtos['bill'],
        sell_payload=builded_dtos['sell'],
        client_payload=builded_dtos['client']
    )
