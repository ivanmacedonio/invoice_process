from abc import abstractmethod, ABC


class IBilling(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def create_and_get_queues(self):
        pass

    @abstractmethod
    def create_and_get_dispatchers(self, tasks):
        if not tasks:
            raise TypeError('tasks arg is required')
        pass

    @abstractmethod
    def create_and_get_threads(self, dispatchers):
        if not dispatchers:
            raise TypeError('dispatchers is required')
        pass

    @abstractmethod
    def set_tasks(self, tasks):
        if not tasks:
            raise TypeError('tasks is required')
        pass

    @abstractmethod
    def run(self):
        pass
