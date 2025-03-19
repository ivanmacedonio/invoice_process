from app.services.thread_pool import Queue, Dispatcher
from app.factories.worker_factory import WorkerFactory
from app.configs.environments import WORKERS_AMOUNT
from app.configs.logger import logger
from app.interfaces.billing_interface import IBilling, IQueueManager, ITaskDispatcher, IThreadManager

class BillingFacade(IBilling):
    def __init__(self, workers_amount):
        self.tasks = []
        self.workers_amount = workers_amount
        self.queue_manager = QueueManager(workers_amount)
        self.thread_manager = None
        self.task_dispatcher = None

    def set_tasks(self, tasks: list):
        self.tasks = tasks

    def run(self):
        task_queues = self.queue_manager.create_queues()
        self.task_dispatcher = TaskDispatcher(
            self.workers_amount, task_queues)
        self.task_dispatcher.dispatch(self.tasks)

        self.thread_manager = ThreadManager(
            self.workers_amount, task_queues)

        workers_factory = WorkerFactory()
        threads = self.thread_manager.create_and_run_threads(
            factory=workers_factory)

        for thread in threads:
            thread.join()

        logger.info(
            f"Billing process ended. Sending summary to Discord.")


class QueueManager(IQueueManager):
    def __init__(self, workers_amount):
        self.workers_amount = workers_amount

    def create_queues(self):
        queue_instance = Queue()
        return queue_instance.build_queues(self.workers_amount)


class TaskDispatcher(ITaskDispatcher):
    def __init__(self, workers_amount, task_queues):
        self.workers_amount = workers_amount
        self.task_queues = task_queues

    def dispatch(self, tasks):
        dispatcher = Dispatcher(self.workers_amount, self.task_queues)
        dispatcher.dispatch(tasks)


class ThreadManager(IThreadManager):
    def __init__(self, workers_amount, task_queues):
        self.workers_amount = workers_amount
        self.task_queues = task_queues

    def create_and_run_threads(self, factory):
        dispatchers = Dispatcher(self.workers_amount, self.task_queues)
        threads = dispatchers.create_and_run_threads(factory)
        return threads
