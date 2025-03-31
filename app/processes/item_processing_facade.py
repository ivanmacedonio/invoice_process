from app.configs.logger import logger
from afip import Afip
from threading import Lock
from app.services.bill_print import BillPrint
from app.services.database import Database
from app.services.arca import BillingService, BuildManager, InstanceManager
from app.repositories.bill_repository import BillRepository, IBillRepository
from app.builders.bill_builder import BillBuilder
from app.services.email import EmailService
from app.decorators.error_handling_provider import error_handling_provider
from app.entities.enums.payclub_status_enum import PayclubTransactionStatus

instance_lock = Lock()


@error_handling_provider
def process_transaction_facade(transaction):
    logger.info(f'Iterating over the follow transaction: {transaction}')

    if not is_transaction_approved and transaction_was_already_invoiced():
        return

    # TODO: REMOVE WHEN PAYCLUB ADD THE NECESSARY FIELDS
    transaction['domicilio'] = "Calle falsa 123"
    transaction['codigo_postal'] = 123
    transaction['provincia'] = "Buenos Aires"
    transaction['customerEmail'] = "ivanmacedonio778@gmail.com"

    arca_instance = get_or_create_arca_instance()
    with instance_lock:
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


def is_transaction_approved(transaction):
    if transaction.get("status") != PayclubTransactionStatus.CONFIRMED.value:
        logger.info(
            "Current transaction is not confirmed, skipping to the next one")
        return False
    return True


def transaction_was_already_invoiced(transaction):
    repository = get_or_create_repository()
    return repository.bill_was_already_invoiced(transaction.get('txid'))


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
