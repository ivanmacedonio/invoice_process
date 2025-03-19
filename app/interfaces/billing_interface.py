from abc import abstractmethod, ABC


class IBilling(ABC):

    @abstractmethod
    def __init__(self, workers_amount: int):
        if not workers_amount:
            raise ValueError("workers_amount are required")
        pass

    @abstractmethod
    def set_tasks(self, tasks):
        if not tasks:
            raise TypeError('tasks is required')
        pass

    @abstractmethod
    def run(self):
        pass


class IQueueManager(ABC):

    @abstractmethod
    def __init__(self, workers_amount):
        if not workers_amount:
            raise ValueError("workers_amount is required")
        pass

    @abstractmethod
    def create_queues(self):
        pass


class ITaskDispatcher(ABC):

    @abstractmethod
    def __init__(self, workers_amount: int, task_queues):
        if not all([workers_amount, task_queues]):
            raise ValueError('workers_amount and task_queues are required')
        pass

    @abstractmethod
    def dispatch(self, tasks):
        if not tasks:
            raise ValueError('tasks are required')
        pass


class IThreadManager(ABC):

    @abstractmethod
    def __init__(self, workers_amount, task_queues):
        if not all([workers_amount, task_queues]):
            raise ValueError('workers_amount and task_queues are required')
        pass

    @abstractmethod
    def create_and_run_threads(self):
        pass
