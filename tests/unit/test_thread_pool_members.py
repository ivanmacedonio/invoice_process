
import queue
from copy import copy
from unittest import TestCase
from app.factories.worker_factory import WorkerFactory
from app.services.concurrency import Worker, Dispatcher, Queue
from app.interfaces.thread_pool_interface import IQueue


class TestThreadPool(TestCase):

    @classmethod
    def setup_queue(self):
        queue_instance = Queue().build_queues(workers_amount=1)[0]
        self.queue_instance = queue_instance

    @classmethod
    def setup_worker(self):
        def process_method(x): return x
        self.worker_instance = Worker(
            worker_id=1, task_queue=self.queue_instance, process_method=process_method)

    @classmethod
    def setup_dispatcher(self):
        queues = Queue().build_queues(workers_amount=3)
        self.dispatcher_instance = Dispatcher(
            workers_amount=3, task_queues=queues)

    @classmethod
    def setup_worker_factory(self):
        self.worker_factory = WorkerFactory()

    @classmethod
    def setUp(self):
        self.setup_queue()
        self.setup_worker()
        self.setup_dispatcher()

    def test_thread_pool_setup_successfully(self):
        self.assertIsNotNone(self.queue_instance)
        self.assertIsNotNone(self.worker_instance)
        self.assertIsNotNone(self.dispatcher_instance)

    def test_queue_works_successfully(self):
        queue_cpy: IQueue = copy(self.queue_instance)

        self.assertIsNotNone(queue_cpy)
        self.assertTrue(type(queue_cpy) == queue.Queue)

    def test_dispatcher_was_builded_successfully(self):
        dispatcher_cpy = copy(self.dispatcher_instance)

        self.assertIsNotNone(dispatcher_cpy)
        self.assertIsNotNone(dispatcher_cpy.workers_amount)
        self.assertIsNotNone(dispatcher_cpy.task_queues)

        self.assertTrue(hasattr(dispatcher_cpy, "dispatch"))
        self.assertTrue(hasattr(dispatcher_cpy, "create_and_run_threads"))

    def test_dispatcher_distributes_the_tasks_successfully(self):
        tasks_to_enqueue = ['item_1', 'item_2', 'item_3']
        dispatcher_cpy = copy(self.dispatcher_instance)
        dispatcher_cpy.dispatch(tasks_to_enqueue)

        for queue in dispatcher_cpy.task_queues:
            self.assertEqual(queue.qsize(), 1)

    def test_worker_process_items_successfully(self):
        queue_cpy = copy(self.queue_instance)
        queue_cpy.put('item 1')
        queue_cpy.put('item 2')
        queue_cpy.put('item 3')

        worker_cpy = copy(self.worker_instance)
        worker_cpy.task_queue = queue_cpy
        worker_cpy.run()

        self.assertTrue(hasattr(worker_cpy, "worker_id"))
        self.assertTrue(hasattr(worker_cpy, "task_queue"))
        self.assertTrue(hasattr(worker_cpy, "process_method"))

        self.assertEqual(queue_cpy.qsize(), 0)

    def test_dispatcher_run_and_closes_threads_successfully(self):
        self.setup_worker_factory()

        dispatcher_cpy = copy(self.dispatcher_instance)
        dispatcher_cpy.create_and_run_threads(self.worker_factory)
        threads = dispatcher_cpy.threads

        self.assertIsNotNone(dispatcher_cpy)
        self.assertTrue(len(threads) == dispatcher_cpy.workers_amount)

        for i in range(dispatcher_cpy.workers_amount):
            self.assertTrue(threads[i].is_alive())

        for i in range(dispatcher_cpy.workers_amount):
            threads[i].join()

        for i in range(dispatcher_cpy.workers_amount):
            self.assertFalse(threads[i].is_alive())
