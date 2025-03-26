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


def get_or_create_session():
    return SingletonManager.get_or_create_instance('database', lambda: Database().get_local_session())


def get_or_create_repository():
    session = get_or_create_session()
    return SingletonManager.get_or_create_instance('bill_repository', lambda: BillRepository(session=session))


def get_or_create_arca_instance():
    repository = get_or_create_repository()
    instance_manager = InstanceManager(billing_processor=Afip)
    builder_manager = BuildManager()
    return SingletonManager.get_or_create_instance('arca_instance', lambda: BillingService(instance_manager, builder_manager, repository))


@error_handling_provider
def process_transaction_facade(transaction):
    # billing stuff
    arca_instance = get_or_create_arca_instance()
    arca_response = arca_instance.bill(transaction)

    # querying stuff
    repository: IBillRepository = get_or_create_repository()
    client_dto, sell_dto, bill_dto = BillBuilder().build_dtos(
        transaction=transaction,
        bill_data=arca_response['builded_bill']
    )
    bill_creation_querie_response = repository.create_bill(
        bill_payload=bill_dto,
        sell_payload=sell_dto,
        client_payload=client_dto
    )

    bill_summary: dict = {
        "payclub_transaction_id":  transaction.get('txid', "Payclub ID does not provided"),
        "arca_response": arca_response['message'],
        "database_querie_response": bill_creation_querie_response
    }
    logger.info(f'Billing response: {bill_summary}')
