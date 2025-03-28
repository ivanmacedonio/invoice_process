from unittest import TestCase
from afip import Afip
from app.services.database import Database
from app.services.arca import BillingService, InstanceManager, BuildManager
from app.repositories.bill_repository import BillRepository


class TestBillingService(TestCase):

    def setUp(self):
        db_session = Database().create_session()
        instance_manager = InstanceManager(
            billing_processor=Afip
        )
        build_manager = BuildManager()
        repository = BillRepository(
            session=db_session
        )
        self.billing_service = BillingService(
            builder_manager=build_manager,
            instance_manager=instance_manager,
            repository=repository
        )

    def test_arca_billing_works_successfully(self):
        dummy_transaction = {
            "amount": 1000,
        }
        arca_response = self.billing_service.bill(
            transaction=dummy_transaction
        )

        self.assertTrue('CAE' in arca_response['cae_data'])
        self.assertTrue('CAEFchVto' in arca_response['cae_data'])
        self.assertTrue(isinstance(arca_response['cae_data'], dict))
