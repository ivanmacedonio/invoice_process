from abc import abstractmethod, ABC


class IProcessRunner(ABC):

    @abstractmethod
    def __init__(self, workers_amount, queue_manager, task_dispatcher, thread_manager, factory):
        pass

    @abstractmethod
    def set_tasks(self, tasks):
        pass

    @abstractmethod
    def run(self):
        pass


class IQueueManager(ABC):

    @abstractmethod
    def create_queues(self, workers_amount: int):
        pass


class ITaskDispatcher(ABC):

    @abstractmethod
    def dispatch(self, workers_amount, queues, tasks):
        if not tasks:
            raise ValueError('tasks are required')
        pass


class IThreadManager(ABC):

    @abstractmethod
    def create_and_run_threads(self, workers_amount, factory, queues):
        pass
