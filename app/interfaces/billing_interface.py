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
        pass

    @abstractmethod
    def create_and_get_threads(self, dispatchers):
        pass

    @abstractmethod
    def set_tasks(self, tasks):
        pass

    @abstractmethod
    def run(self):
        pass
