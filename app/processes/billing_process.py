from app.repositories.payclub_repository import PayclubRepository
from app.services.concurrency import ProcessRunner, QueueManager, TaskDispatcher, ThreadManager, WorkerFactory
from app.services.payclub import PayclubService
from app.decorators.error_handling_provider import error_handling_provider
from app.configs.environments import WORKERS_AMOUNT
from app.configs.environments import WORKERS_AMOUNT


def setup_and_get_payclub_instance():
    payclub_repository_instance = PayclubRepository()
    payclub_instance = PayclubService(payclub_repository_instance)
    return payclub_instance


def get_transactions_strategy(custom_dates: dict):
    payclub_instance = setup_and_get_payclub_instance()
    # query README.md to view the wished format of the dates
    dates_were_received = all(key in custom_dates for key in [
                              'dateFrom', 'dateTo'])
    if dates_were_received:
        return payclub_instance.get_transactions_by_date(date_from=custom_dates['dateFrom'], date_to=custom_dates['dateTo'])
    else:
        return payclub_instance.get_last_24_hours_transactions()


@error_handling_provider
def billing_process_facade(args):
    transactions = get_transactions_strategy(custom_dates=args.to_dict())

    queue_manager = QueueManager()
    task_dispatcher = TaskDispatcher()
    thread_manager = ThreadManager()
    factory = WorkerFactory()

    concurrent_process_runner = ProcessRunner(
        WORKERS_AMOUNT, queue_manager, task_dispatcher, thread_manager, factory)
    concurrent_process_runner.set_tasks(transactions)
    concurrent_process_runner.run()
