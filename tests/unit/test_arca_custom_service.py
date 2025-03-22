from unittest import TestCase
from unittest.mock import MagicMock
from app.services.arca import BillingService, BuildManager, InstanceManager
from app.repositories.bill_repository import BillRepository


class TestArcaCustomService(TestCase):

    def set_up_mocked_repository(self):
        mocked_repository = MagicMock(spec=BillRepository)
        self.mocked_repository = mocked_repository

    def set_up_mocked_instance_manager(self):
        mocked_instance_manager = MagicMock(spec=InstanceManager)
        self.mocked_instance_manager = mocked_instance_manager

    def set_up_mocked_builder_manager(self):
        builder_manager = BuildManager()
        self.builder_manager = builder_manager

    def set_up_mocked_billing_service(self):
        self.mocked_billing_service = BillingService(
            builder_manager=self.builder_manager,
            repository=self.mocked_repository,
            instance_manager=self.mocked_instance_manager
        )

    def setUp(self):
        self.set_up_mocked_repository()
        self.set_up_mocked_instance_manager()
        self.set_up_mocked_builder_manager()
        self.set_up_mocked_billing_service()

    def test_bill_builder_works_successfully(self):
        pass
