import traceback
from app.configs.logger import logger
from app.services.database import Database
from app.services.arca import BillingService, BuildManager, InstanceManager
from app.repositories.bill_repository import BillRepository
from sqlalchemy.exc import IntegrityError, DisconnectionError, SQLAlchemyError, DatabaseError, ArgumentError
from threading import Lock


_lock = Lock()


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
    instance_manager = InstanceManager()
    builder_manager = BuildManager()
    return SingletonManager.get_or_create_instance('arca_instance', lambda: BillingService(instance_manager, builder_manager, repository))


def process_bill_facade(transaction):
    try:
        with _lock:
            arca_instance = get_or_create_arca_instance()
        bill_response = arca_instance.bill(transaction)

    except SQLAlchemyError as sqle:
        logger.error(traceback.format_exc())
        logger.error(f'Unexpected SQLAlchemy error: {sqle}')

    except DisconnectionError as sqlderr:
        logger.error(traceback.format_exc())
        logger.error(f'SQLAlchemy lost the database connection: {sqlderr}')

    except IntegrityError as sqlierr:
        logger.error(traceback.format_exc())
        logger.error(f'SQLAlchemy Unexpected Integrity error: {sqlierr}')

    except DatabaseError as sqldberr:
        logger.error(traceback.format_exc())
        logger.error(f'SQLAlchemy Unexpected Database error: {sqldberr}')

    except ArgumentError as sqlargerr:
        logger.error(traceback.format_exc())
        logger.error(f'SQLAlchemy Unexpected Database error: {sqlargerr}')
