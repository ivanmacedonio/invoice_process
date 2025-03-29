from app.configs.logger import logger
from afip import Afip
from app.services.bill_print import BillPrint
from app.services.database import Database
from app.services.arca import BillingService, BuildManager, InstanceManager
from app.repositories.bill_repository import BillRepository, IBillRepository
from app.services.email import EmailService
from app.builders.bill_builder import BillBuilder
from app.decorators.error_handling_provider import error_handling_provider


@error_handling_provider
def process_transaction_facade(transaction):
    logger.info(f'Iterating over the follow transaction: {transaction}')

    arca_instance = get_or_create_arca_instance()
    arca_response = arca_instance.bill(transaction)

    builded_dtos = create_and_push_to_db_facade(
        arca_response=arca_response,
        transaction=transaction
    )

    binary_pdf = create_binary_pdf(
        builded_dtos=builded_dtos
    )

    EmailService().send_email(
        to_email=transaction.get("customerEmail"),
        b64_pdf=binary_pdf
    )


def create_and_push_to_db_facade(transaction, arca_response):
    repository: IBillRepository = get_or_create_repository()
    builded_dtos = BillBuilder().build_dtos(
        transaction=transaction,
        bill_data=arca_response['builded_bill'],
        invoicer_data=arca_response['invoicer_data'],
        cae_data=arca_response['cae_data']
    )
    repository.create_bill(
        bill_payload=builded_dtos['bill'],
        sell_payload=builded_dtos['sell'],
        client_payload=builded_dtos['client']
    )
    return builded_dtos


def create_binary_pdf(builded_dtos):
    binnary_pdf = BillPrint(
        payload=builded_dtos['bill_to_print']).write_and_get_binary_pdf()
    return binnary_pdf


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
