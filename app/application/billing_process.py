from app.adapters.outbound.repositories.Mercadopago_repository import MercadopagoRepository
from app.domain.services.concurrency import ProcessRunner, QueueManager, TaskDispatcher, ThreadManager, WorkerFactory
from app.domain.services.wallet import MercadopagoService
from app.domain.services.discord import Discord, CounterManager
from app.domain.entities.dataclasses.discord_message_dataclass import DiscordMessagePayload
from app.domain.decorators.error_handling_provider import error_handling_provider
from app.config.dependencies import WORKERS_AMOUNT
from app.config.logger import logger
from functools import partial
from datetime import datetime


@error_handling_provider
def billing_process_facade(args):
    queue_manager = QueueManager()
    task_dispatcher = TaskDispatcher()
    thread_manager = ThreadManager()
    factory = WorkerFactory()

    concurrent_process_runner = ProcessRunner(
        WORKERS_AMOUNT, queue_manager, task_dispatcher, thread_manager, factory, callback=partial(
            start_process_runner,
            args=args
        ))

    start_process_runner(concurrent_process_runner, args)

    logger.info(f"Billing proceess ended, sending summary to Discord...")
    Discord().post(embeds=build_discord_message())


def start_process_runner(process_runner, args):
    transactions = get_transactions_strategy(custom_dates=args.to_dict())
    process_runner.set_tasks(transactions)
    process_runner.run()


Mercadopago_instance = None


def setup_and_get_Mercadopago_instance():
    global Mercadopago_instance
    if not Mercadopago_instance:
        Mercadopago_repository_instance = MercadopagoRepository()
        Mercadopago_instance = MercadopagoService(Mercadopago_repository_instance)
    return Mercadopago_instance


def get_transactions_strategy(custom_dates: dict):
    Mercadopago_instance = setup_and_get_Mercadopago_instance()
    # query README.md to view the wished format of the dates
    dates_were_received = all(key in custom_dates for key in [
                              'dateFrom', 'dateTo'])
    if dates_were_received:
        return Mercadopago_instance.get_transactions_by_date(date_from=custom_dates['dateFrom'], date_to=custom_dates['dateTo'])
    else:
        return Mercadopago_instance.get_last_24_hours_transactions()


def build_discord_message():
    today = datetime.now()
    amounts = CounterManager().get_amounts()
    return DiscordMessagePayload(
        title="Resumen de facturación de créditos Mercadopago",
        description=f'Resumen del día: {str(today)}',
        total_invoices_count=amounts['total'],
        approved_invoices_count=amounts['approved'],
        rejected_invoices_count=amounts['total'] - amounts['approved'],
        invoiced_amount=amounts['money_amount']
    )
