from app.configs.logger import logger
from afip import Afip
from threading import Lock
from app.services.bill_print import BillPrint
from app.services.database import Database
from app.services.arca import BillingService, BuildManager, InstanceManager
from app.repositories.bill_repository import BillRepository, IBillRepository
from app.builders.bill_builder import BillBuilder
from app.services.email import EmailService
from app.services.discord import CounterManager
from app.decorators.error_handling_provider import error_handling_provider
from app.entities.enums.payclub_status_enum import PayclubTransactionStatus
from app.entities.enums.payclub_product_type import PayclubProductTypeEnum
from app.utils.custom_exceptions import AlreadyInvoicedException, RejectedTransaction, InvalidTransactionType
from app.utils.validate_fields import validate_fields

instance_lock = Lock()  # create a lock to avoid the starvation and race condition


@error_handling_provider
def process_transaction_facade(transaction):
    skip_if_transaction_is_invalid(transaction)

    with instance_lock:
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

    CounterManager().push_approved(1).push_money_amount(transaction['amount'])


def skip_if_transaction_is_invalid(transaction):
    if not is_received_points_product(transaction):
        raise InvalidTransactionType(transaction)

    if not is_transaction_approved(transaction):
        raise RejectedTransaction(transaction)

    if transaction_was_already_invoiced(transaction):
        raise AlreadyInvoicedException(transaction)

    validate_transaction_fields(transaction)


def is_transaction_approved(transaction):
    return transaction.get("status") == PayclubTransactionStatus.CONFIRMED.value


def transaction_was_already_invoiced(transaction):
    repository = get_or_create_repository()
    was_already_invoiced = repository.bill_was_already_invoiced(
        transaction.get('txid'))
    return was_already_invoiced


def is_received_points_product(transaction):
    return transaction.get('product') == PayclubProductTypeEnum.RECEIVED_POINTS.value


def validate_transaction_fields(transaction):
    validate_fields(target_fields={
        "txid": transaction['txid'],
        "product": transaction['product'],
        "customerNin": transaction['customerNin'],
        "customerEmail": transaction['customerEmail'],
        "amount": transaction['amount'],
        "storeName": transaction['storeName'],
        "status": transaction['status'],
    }, error_message="missing fields while trying to process the transaction. Skipping to the next one")


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
