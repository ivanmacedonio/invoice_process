from app.domain.interfaces.thread_pool_interface import IWorkerFactory, IWorker
import queue


class WorkerFactory(IWorkerFactory):

    def build_worker(self, worker_id: int, task_queue: queue.Queue, process_method) -> IWorker:
        from app.domain.services.concurrency import Worker
        return Worker(worker_id, task_queue, process_method)
