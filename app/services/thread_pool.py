import threading
import queue

from configs.logger import logger
from interfaces.thread_pool_interface import IQueue, IWorker, IDispatcher, IWorkerFactory


class Queue(IQueue):

    def __init__(self):
        self.task_queues = None

    @classmethod
    def set_task_queues(self, new_task_queues):
        self.task_queues = new_task_queues

    def get_task_queues(self):
        return self.task_queues

    def build_queues(self, workers_amount):
        task_queues = [queue.Queue() for _ in range(int(workers_amount))]
        self.set_task_queues(task_queues)
        return task_queues


class Worker(IWorker):

    def __init__(self, worker_id, task_queue, lock):
        self.worker_id = worker_id
        self.task_queue = task_queue
        self.lock = lock

    def process_item(self, item):
        with self.lock:
            logger.info(f'Processing {item}')

    def run(self):
        while True:
            try:
                item = self.task_queue.get(timeout=10)
            except queue.Empty:
                break

            self.process_item(item)
            self.task_queue.task_done()


class WorkerFactory(IWorkerFactory):

    def build_worker(self, worker_id, task_queue, lock_instance):
        return Worker(worker_id, task_queue, lock_instance)


class Dispatcher(IDispatcher):

    def __init__(self, workers_amount, task_queues):
        self.workers_amount = int(workers_amount)
        self.task_queues = task_queues
        self.lock = threading.Lock()

    def dispatch(self, tasks):
        for i, item in enumerate(tasks):
            self.task_queues[i % self.workers_amount].put(item)

    def create_workers(self, worker_factory):
        threads = []
        for i in range(self.workers_amount):
            worker = worker_factory.build_worker(
                i, self.task_queues[i], self.lock)
            thread = threading.Thread(target=worker.run)
            thread.start()
            threads.append(thread)
        return threads
