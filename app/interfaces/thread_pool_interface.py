from abc import abstractmethod, ABC


class IQueue(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def set_task_queues(self, new_task_queues):
        pass

    @abstractmethod
    def get_task_queues(self):
        pass

    @abstractmethod
    def build_queues(self, workers_amount):
        pass


class IWorker(ABC):

    @abstractmethod
    def __init__(self, worker_id, task_queue):
        pass

    @abstractmethod
    def process_item(self, item):
        pass

    @abstractmethod
    def run(self):
        pass


class IWorkerFactory(ABC):

    @abstractmethod
    def build_worker(self, worker_id, task_queue):
        pass


class IDispatcher(ABC):

    @abstractmethod
    def __init__(self, workers_amount, task_queues):
        pass

    @abstractmethod
    def dispatch(self, tasks):
        pass

    @abstractmethod
    def create_and_run_threads(self, worker_factory):
        pass
