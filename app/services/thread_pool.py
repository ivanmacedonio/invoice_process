import threading
import queue
from typing import Union, Optional

from app.configs.logger import logger
from app.interfaces.thread_pool_interface import IQueue, IWorker, IDispatcher, IWorkerFactory
from app.processes.process_item import process_item


class Queue(IQueue):

    def __init__(self):
        self.task_queues = None

    @classmethod
    def set_task_queues(self, new_task_queues: list[queue.Queue]):
        self.task_queues = new_task_queues

    def get_task_queues(self) -> list[queue.Queue]:
        return self.task_queues

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
                item = self.task_queue.get(timeout=10)
            except queue.Empty:
                break

            self.process_method(item)
            self.task_queue.task_done()


class Dispatcher(IDispatcher):

    def __init__(self, workers_amount: Union[str | int], task_queues: Optional[list[queue.Queue]]):
        self.workers_amount = int(workers_amount)
        self.task_queues = task_queues

    def dispatch(self, tasks: list[object]):
        for i, item in enumerate(tasks):
            self.task_queues[i % self.workers_amount].put(item)

    def create_and_run_threads(self, worker_factory: IWorkerFactory):
        threads = []
        for i in range(self.workers_amount):
            worker = worker_factory.build_worker(
                i, self.task_queues[i], process_item)
            thread = threading.Thread(target=worker.run)
            thread.start()
            threads.append(thread)
        return threads
