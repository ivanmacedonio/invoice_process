from repositories.payclub_repository import PayclubRepository
from services.billing import Billing
from services.payclub import PayclubService
from decorators.error_handling_provider import error_handling_provider


def setup_and_get_payclub_instance():
    payclub_repository_instance = PayclubRepository()
    payclub_instance = PayclubService(payclub_repository_instance)
    return payclub_instance


def get_transactions_strategy(custom_dates: dict):
    payclub_instance = setup_and_get_payclub_instance()

    # query README.md to view the wished format of the dates
    dates_were_received = all(key in custom_dates for key in ['dateFrom', 'dateTo'])
    if dates_were_received:
        return payclub_instance.get_transactions_by_date(date_from=custom_dates['dateFrom'], date_to=custom_dates['dateTo'])
    else:
        return payclub_instance.get_last_24_hours_transactions()


@error_handling_provider
def billing_process(args):
    transactions = get_transactions_strategy(args.to_dict())

    billing_instance = Billing()
    billing_instance.set_tasks(transactions)
    billing_instance.run()
