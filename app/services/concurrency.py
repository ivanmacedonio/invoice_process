from app.configs.logger import logger
from app.factories.worker_factory import WorkerFactory
from app.interfaces.concurrency_interface import IProcessRunner, IQueueManager, ITaskDispatcher, IThreadManager
import threading
import queue
from typing import Union, Optional
from app.interfaces.thread_pool_interface import IQueue, IWorker, IDispatcher, IWorkerFactory
from app.processes.item_processing_facade import process_transaction_facade


class ProcessRunner(IProcessRunner):
    def __init__(self, workers_amount, queue_manager, task_dispatcher, thread_manager, factory, callback):
        self.tasks = []
        self.workers_amount = workers_amount
        self.queue_manager = queue_manager
        self.thread_manager = thread_manager
        self.task_dispatcher = task_dispatcher
        self.factory = factory
        self.callback = callback

    def set_tasks(self, tasks: list):
        self.tasks = tasks

    def run(self):
        if not self.tasks:
            return

        task_queues = self.queue_manager.create_queues(self.workers_amount)
        self.task_dispatcher.dispatch(
            self.workers_amount, task_queues, self.tasks)
        threads = self.thread_manager.create_and_run_threads(
            self.workers_amount, self.factory, task_queues)

        for thread in threads:
            thread.join()

        if self.callback:
            self.callback(self)


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


class Queue(IQueue):

    def __init__(self):
        self.task_queues = None

    @classmethod
    def set_task_queues(self, new_task_queues: list[queue.Queue]):
        self.task_queues = new_task_queues

    def build_queues(self, workers_amount: Union[str | int]) -> list[queue.Queue]:
        task_queues = [queue.Queue() for _ in range(int(workers_amount))]
        self.set_task_queues(task_queues)
        return task_queues


class Worker(IWorker):

    def __init__(self, worker_id: int, task_queue: queue.Queue, process_method):
        self.worker_id = worker_id
        self.task_queue = task_queue
        self.process_method = process_method

    def run(self):
        while True:
            try:
                item = self.task_queue.get(timeout=3)
            except queue.Empty:
                break

            self.process_method(item)
            self.task_queue.task_done()


class Dispatcher(IDispatcher):

    def __init__(self, workers_amount: Union[str | int], task_queues: Optional[list[queue.Queue]]):
        self.threads = []
        self.workers_amount = int(workers_amount)
        self.task_queues = task_queues

    def dispatch(self, tasks: list[object]):
        for i, item in enumerate(tasks):
            self.task_queues[i % self.workers_amount].put(item)

    def create_and_run_threads(self, worker_factory: IWorkerFactory):
        for i in range(self.workers_amount):
            worker = worker_factory.build_worker(
                i, self.task_queues[i], process_transaction_facade)
            thread = threading.Thread(target=worker.run)
            thread.start()
            self.threads.append(thread)
        return self.threads
