import traceback
import requests
from app.configs.logger import logger
from sqlalchemy.exc import SQLAlchemyError, DisconnectionError, IntegrityError, DatabaseError, ArgumentError
from mailchimp_transactional.api_client import ApiClientError
from app.utils.custom_exceptions import AlreadyInvoicedException, InvalidTransactionType, RejectedTransaction


def error_handling_provider(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError as ve:
            logger.error(traceback.format_exc())
            logger.error(f'Unexpected Value error: {ve}')

        except TypeError as te:
            logger.error(traceback.format_exc())
            logger.error(f'Unexpected Type error: {te}')

        except KeyError as ke:
            logger.error(traceback.format_exc())
            logger.error(f'Unexpected Key error: {ke}')

        except AttributeError as ae:
            logger.error(traceback.format_exc())
            logger.error(f'Unexpected Attribute error: {ae}')

        except requests.RequestException as re:
            logger.error(traceback.format_exc())
            logger.error(f'Unexpected request error: {re}')

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

        except ApiClientError as emaile:
            logger.error(traceback.format_exc())
            logger.error(
                f'Unexpected Mailchimp error while trying to send the bill via email: {emaile.text}')

        except (RejectedTransaction, AlreadyInvoicedException) as e:
            logger.info(f'{e}: Skipping to the next transaction')

        except InvalidTransactionType:
            pass

        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error(f'Unexpected unhandled exception: {e}')

    return wrapper
