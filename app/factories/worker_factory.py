from interfaces.thread_pool_interface import IWorkerFactory, IWorker
from services.thread_pool import Worker
import queue


class WorkerFactory(IWorkerFactory):

    def build_worker(self, worker_id: int, task_queue: queue.Queue) -> IWorker:
        return Worker(worker_id, task_queue)
