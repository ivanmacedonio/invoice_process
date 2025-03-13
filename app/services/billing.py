from services.thread_pool import Queue, Dispatcher
from factories.worker_factory import WorkerFactory
from configs.environments import WORKERS_AMOUNT
from configs.logger import logger
from interfaces.billing_interface import IBilling


class Billing(IBilling):

    def __init__(self):
        self.tasks = []

    @classmethod
    def create_and_get_queues(self):
        queue_instance = Queue()
        task_queues = queue_instance.build_queues(WORKERS_AMOUNT)
        return task_queues

    @classmethod
    def create_and_get_dispatchers(self, tasks):
        task_queues = self.create_and_get_queues()
        dispatchers = Dispatcher(WORKERS_AMOUNT, task_queues)
        dispatchers.dispatch(tasks)
        return dispatchers

    @classmethod
    def create_and_get_threads(self, dispatchers):
        worker_factory = WorkerFactory()
        threads = dispatchers.create_and_run_threads(worker_factory)
        return threads

    def set_tasks(self, tasks):
        self.tasks = tasks

    def run(self):
        dispatchers = self.create_and_get_dispatchers(self.tasks)
        threads = self.create_and_get_threads(dispatchers)

        for thread in threads:
            thread.join()

        logger.info("Billing process ended")
