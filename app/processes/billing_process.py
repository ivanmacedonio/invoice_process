from services.thread_pool import Queue, Dispatcher, WorkerFactory
from configs.environments import WORKERS_AMOUNT
from configs.logger import logger


def setup_task_queues():
    queue_instance = Queue()
    task_queues = queue_instance.build_queues(WORKERS_AMOUNT)
    return task_queues


def setup_dispatchers(tasks):
    task_queues = setup_task_queues()
    dispatchers = Dispatcher(WORKERS_AMOUNT, task_queues)
    dispatchers.dispatch(tasks)
    return dispatchers


def setup_threads_and_workers(dispatchers):
    worker_factory = WorkerFactory()
    threads = dispatchers.create_workers(worker_factory)
    return threads


def billing_process():

    tasks = [f'task {i}' for i in range(20)]

    dispatchers = setup_dispatchers(tasks)
    threads = setup_threads_and_workers(dispatchers)

    for thread in threads:
        thread.join()

    logger.info("Billing process ended")
