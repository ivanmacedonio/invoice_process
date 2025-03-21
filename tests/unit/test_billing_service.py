from copy import copy
from unittest import TestCase
from unittest.mock import MagicMock
from app.services.billing import BillingFacade, QueueManager, TaskDispatcher, ThreadManager


class TestBillingService(TestCase):

    def set_up_dummy_queue_manager(self):
<<<<<<< HEAD
        self.dummy_queue_manager = QueueManager()

    def set_up_dummy_task_dispatcher(self):
        self.dummy_task_dispatcher = TaskDispatcher()

    def set_up_dummy_thread_manager(self):
        self.dummy_thread_manager = ThreadManager()

    def set_up_factory_mock(self):
        self.dummy_factory = MagicMock()
        self.dummy_worker = MagicMock()

        self.dummy_worker.run.return_value = lambda x: x
        self.dummy_factory.build_worker.return_value = self.dummy_worker

    def setUp(self):
        self.set_up_dummy_queue_manager()
        self.set_up_dummy_task_dispatcher()
        self.set_up_dummy_thread_manager()
        self.set_up_factory_mock()

        self.billing_service = BillingFacade(
            workers_amount=2,
            queue_manager=self.dummy_queue_manager,
            task_dispatcher=self.dummy_task_dispatcher,
            thread_manager=self.dummy_thread_manager,
            factory=self.dummy_factory
        )

=======
        workers_amount = 2
        self.dummy_queue_manager = QueueManager(workers_amount)

    def set_up_dummy_task_dispatcher(self, workers_amount, queues):
        self.dummy_task_dispatcher = TaskDispatcher(
            workers_amount=workers_amount, task_queues=queues)

    def set_up_dummy_thread_manager(self, workers_amount, queues):
        self.dummy_thread_manager = ThreadManager(
            workers_amount=workers_amount, task_queues=queues)

    def setUp(self):
        self.set_up_dummy_queue_manager()
        self.billing_service = BillingFacade(workers_amount=1)
>>>>>>> b17b2eb1935242b3a08771d8dfc1d96747898e6d
        self.dummy_tasks = ['item_a', 'item_b', 'item_c', 'item_d']

    def test_billing_service_set_tasks_successfully(self):
        billing_cpy = copy(self.billing_service)
        billing_cpy.set_tasks(self.dummy_tasks)

        self.assertIsNotNone(billing_cpy)
        self.assertTrue(len(billing_cpy.tasks) > 0)
        self.assertIsNotNone(billing_cpy.tasks)

    def test_queue_manager_works_successfully(self):
        dummy_queue_manager_cpy = copy(self.dummy_queue_manager)
<<<<<<< HEAD
        task_queues = dummy_queue_manager_cpy.create_queues(workers_amount=2)

        self.assertIsNotNone(task_queues)
        self.assertEqual(len(task_queues), 2)  # Validamos que se creen 2 colas

    def test_task_dispatcher_works_successfully(self):
        task_queues = self.dummy_queue_manager.create_queues(workers_amount=2)
        self.dummy_task_dispatcher.dispatch(
            workers_amount=2, queues=task_queues, tasks=self.dummy_tasks)

        for q in task_queues:
            self.assertEqual(q.qsize(), 2)

    def test_thread_manager_works_successfully(self):
        dummy_thread_manager_cpy = copy(self.dummy_thread_manager)
        task_queues = self.dummy_queue_manager.create_queues(workers_amount=2)

        threads = dummy_thread_manager_cpy.create_and_run_threads(
            workers_amount=2, factory=self.dummy_factory, queues=task_queues)
=======
        dummy_queue = dummy_queue_manager_cpy.create_queues()

        self.assertIsNotNone(dummy_queue)
        self.assertTrue(len(dummy_queue) == 2)

    def test_task_dispatcher_works_successfully(self):
        dummy_queue_manager_cpy = copy(self.dummy_queue_manager)
        queues = dummy_queue_manager_cpy.create_queues()
        self.set_up_dummy_task_dispatcher(workers_amount=2, queues=queues)
        dummy_task_dispatcher_cpy = copy(self.dummy_task_dispatcher)
        dummy_task_dispatcher_cpy.dispatch(self.dummy_tasks)

        self.assertIsNotNone(dummy_task_dispatcher_cpy)

        for q in queues:
            # test the task distribution of the dispatcher
            self.assertTrue(q.qsize() == 2)

    def test_thread_manager_works_successfully(self):
        dummy_queue = copy(self.dummy_queue_manager.create_queues())
        self.set_up_dummy_thread_manager(workers_amount=2, queues=dummy_queue)
        dummy_thread_manager_cpy = copy(self.dummy_thread_manager)
        dummy_factory = MagicMock()
        dummy_worker = MagicMock()

        dummy_worker.run.return_value = lambda x: x
        dummy_factory.build_worker.return_value = dummy_worker

        threads = dummy_thread_manager_cpy.create_and_run_threads(
            dummy_factory)
>>>>>>> b17b2eb1935242b3a08771d8dfc1d96747898e6d

        for t in threads:
            t.join()
            self.assertIsNotNone(t)
            self.assertFalse(t.is_alive())
<<<<<<< HEAD
=======

        self.assertEqual(len(dummy_thread_manager_cpy.task_queues), 2)
>>>>>>> b17b2eb1935242b3a08771d8dfc1d96747898e6d
