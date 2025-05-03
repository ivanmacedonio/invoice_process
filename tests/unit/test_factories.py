from unittest import TestCase
from unittest.mock import patch
from app.domain.factories.worker_factory import WorkerFactory
from app.domain.interfaces.thread_pool_interface import IWorker
from queue import Queue


class TestFactories(TestCase):

    def setup_factories(self):
        self.worker_factory_instance = WorkerFactory()

    def setUp(self):
        self.setup_factories()

    def test_worker_factory_works_successfully(self):
        dummy_queue = Queue()

        worker_instance = self.worker_factory_instance.build_worker(
            worker_id=1,
            process_method=lambda x: x,
            task_queue=dummy_queue
        )

        # assert types
        self.assertIsNotNone(worker_instance)
        self.assertIsInstance(worker_instance, IWorker)

        # assert fields builded successfully
        self.assertTrue(hasattr(worker_instance, 'worker_id'))
        self.assertTrue(hasattr(worker_instance, 'process_method'))
        self.assertTrue(hasattr(worker_instance, 'task_queue'))
        self.assertTrue(hasattr(worker_instance, 'run'))
