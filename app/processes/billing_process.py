import requests
import traceback
from repositories.payclub_repository import PayclubRepository
from services.billing import Billing
from services.payclub import PayclubService
from configs.logger import logger
from decorators.error_handling_provider import error_handling_provider


def setup_and_get_payclub_instance():
    payclub_repository_instance = PayclubRepository()
    payclub_instance = PayclubService(payclub_repository_instance)
    return payclub_instance


def get_tasks_to_enqueue():
    payclub_instance = setup_and_get_payclub_instance()
    transactions_history = payclub_instance.get_last_24_hours_transactions()
    return transactions_history


@error_handling_provider
def billing_process():
    tasks = get_tasks_to_enqueue()

    billing_instance = Billing()
    billing_instance.set_tasks(tasks)
    billing_instance.run()
