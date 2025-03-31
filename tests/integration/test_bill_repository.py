from unittest import TestCase
from datetime import datetime
from app.repositories.bill_repository import BillRepository
from app.services.database import Database


class TestBillingService(TestCase):

    def get_or_create_session(self):
        return Database().create_session()

    def set_up_repository(self):
        session = self.get_or_create_session()
        self.repository = BillRepository(
            session=session
        )

    def setUp(self):
        self.set_up_repository()

    def test_get_unique_invoicer_works_successfully(self):
        invoicer_response = self.repository.get_unique_invoicer()

        # Check if required keys are in the invoicer_response
        required_keys = [
            'razon_social', 'ii_bb', 'email', 'punto_de_venta', 'arca_secret_key',
            'arca_certify', 'inicio_actividades', 'id', 'cuit', 'telefono', 'numero_cae', 'fecha_vencimiento_cae'
        ]

        for key in required_keys:
            self.assertTrue(key in invoicer_response)

        # Type checks
        self.assertIsInstance(invoicer_response['cuit'], str)
        self.assertIsInstance(
            invoicer_response['inicio_actividades'], datetime)
        self.assertIsInstance(invoicer_response['ii_bb'], int)
        self.assertIsInstance(
            invoicer_response['fecha_vencimiento_cae'], datetime)
        self.assertIsInstance(invoicer_response['punto_de_venta'], str)
