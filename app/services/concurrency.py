from app.services.thread_pool import Queue, Dispatcher
from app.factories.worker_factory import WorkerFactory
from app.configs.environments import WORKERS_AMOUNT
from app.configs.logger import logger
from app.interfaces.billing_interface import IBilling, IQueueManager, ITaskDispatcher, IThreadManager


class ProcessRunner(IBilling):
    def __init__(self, workers_amount, queue_manager, task_dispatcher, thread_manager, factory):
        self.tasks = []
        self.workers_amount = workers_amount
        self.queue_manager = queue_manager
        self.thread_manager = thread_manager
        self.task_dispatcher = task_dispatcher
        self.factory = factory

    def set_tasks(self, tasks: list):
        self.tasks = tasks

    def run(self):
        task_queues = self.queue_manager.create_queues(self.workers_amount)
        self.task_dispatcher.dispatch(
            self.workers_amount, task_queues, self.tasks)
        threads = self.thread_manager.create_and_run_threads(
            self.workers_amount, self.factory, task_queues)

        for thread in threads:
            thread.join()

        logger.info(
            f"Billing process ended. Sending summary to Discord.")


class QueueManager(IQueueManager):

    def create_queues(self, workers_amount):
        queue_instance = Queue()
        return queue_instance.build_queues(workers_amount)


class TaskDispatcher(ITaskDispatcher):

    def dispatch(self, workers_amount, queues, tasks):
        dispatcher = Dispatcher(workers_amount, queues)
        dispatcher.dispatch(tasks)


class ThreadManager(IThreadManager):

    def create_and_run_threads(self, workers_amount, factory, queues):
        dispatchers = Dispatcher(workers_amount, queues)
        threads = dispatchers.create_and_run_threads(factory)
        return threads
