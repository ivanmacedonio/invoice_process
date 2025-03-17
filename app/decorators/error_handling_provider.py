import traceback
import requests
from app.configs.logger import logger


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

        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error(f'Unexpected unhandled exception: {e}')

    return wrapper
