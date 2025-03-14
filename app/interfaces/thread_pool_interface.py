from abc import abstractmethod, ABC


class IQueue(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def set_task_queues(self, new_task_queues):
        if not new_task_queues:
            raise TypeError('new_task_queues is required')
        pass

    @abstractmethod
    def get_task_queues(self):
        pass

    @abstractmethod
    def build_queues(self, workers_amount):
        if not workers_amount:
            raise TypeError('workers_amount is required')
        pass


class IWorker(ABC):

    @abstractmethod
    def __init__(self, worker_id, task_queue, process_method):
        if not all([worker_id, task_queue, process_method]):
            raise TypeError('lack of arguments while trying to instance Worker class')
        pass

    @abstractmethod
    def run(self):
        pass


class IWorkerFactory(ABC):

    @abstractmethod
    def build_worker(self, worker_id, task_queue, process_method):
        if not all([worker_id, task_queue, process_method]):
            raise TypeError('lack of arguments while trying to execute build_worker')
        pass


class IDispatcher(ABC):

    @abstractmethod
    def __init__(self, workers_amount, task_queues):
        if not workers_amount or task_queues:
            raise TypeError('lack of arguments while trying to instance Dispatcher class')
        pass

    @abstractmethod
    def dispatch(self, tasks):
        if not tasks:
            raise TypeError('tasks is missing')
        pass

    @abstractmethod
    def create_and_run_threads(self, worker_factory):
        if not worker_factory:
            raise TypeError('worker_factory is missing')
        pass
