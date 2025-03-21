import traceback
from app.configs.logger import logger
from app.services.database import Database
from app.services.bill import InvoiceService
from app.services.arca import Arca
from sqlalchemy.exc import IntegrityError, DisconnectionError, SQLAlchemyError, DatabaseError, ArgumentError


def get_or_create_database():
    return Database().get_local_session()


def create_and_get_bill_service_instance():
    bill_service = InvoiceService()
    return bill_service


def create_and_get_arca_instance():
    arca_instance = Arca()
    return arca_instance


def process_bill_facade(item):
    try:
        bill_service = create_and_get_bill_service_instance()
        arca_instance = create_and_get_arca_instance()

        bill_service.execute_billing_with_arca(arca_instance)

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
