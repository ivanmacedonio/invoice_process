import requests
import traceback
from services.billing import Billing
from configs.logger import logger

def billing_process():
    logger.debug(access_token)
    try:
        billing_instance = Billing()
        billing_instance.set_tasks([f'task {i}' for i in range(20)])
        billing_instance.run()

    except ValueError as ve:
        logger.error(traceback.format_exc())
        logger.error(f'Unexpected Value error: {ve}')

    except TypeError as te:
        logger.error(traceback.format_exc())
        logger.error(f'Unexpected Type error: {te}')

    except KeyError as ke:
        logger.error(traceback.format_exc())
        logger.error(f'Unexpected Key error: {ke}')

    except NameError as ne:
        logger.error(traceback.format_exc())
        logger.error(f'Local or global variable name is missing: {ne}')

    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(f'Unexpected unhandled exception: {e}')

    except requests.RequestException as re:
        logger.error(traceback.format_exc())
        logger.error(f'Unexpected request error: {re}')

