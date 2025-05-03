from unittest import TestCase
from datetime import datetime
from unittest.mock import MagicMock
from app.domain.services.arca import BillingService, BuildManager, InstanceManager
from app.adapters.outbound.repositories.bill_repository import BillRepository


class TestArcaCustomService(TestCase):

    def set_up_mocked_repository(self):
        mocked_repository = MagicMock(spec=BillRepository)
        self.mocked_repository = mocked_repository

    def set_up_mocked_instance_manager(self):
        mocked_arca_instance = MagicMock()
        mocked_arca_instance.ElectronicBilling.getLastVoucher.return_value = 0
        self.mocked_arca_instance = mocked_arca_instance

        mocked_instance_manager = MagicMock(spec=InstanceManager)
        mocked_instance_manager.get_or_create_instance.return_value = mocked_arca_instance
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

    def set_up_dummy_transaction(self):
        self.dummy_transaction = {
            "amount": 999
        }

    def set_up_dummy_invoicer(self):
        self.dummy_invoicer = {
            "punto_de_venta": 9,
        }

    def setUp(self):
        self.set_up_mocked_repository()
        self.set_up_mocked_instance_manager()
        self.set_up_mocked_builder_manager()
        self.set_up_mocked_billing_service()
        self.set_up_dummy_transaction()
        self.set_up_dummy_invoicer()

    def test_bill_builder_works_successfully(self):
        today_formatted = int(datetime.today().strftime("%Y%m%d"))

        builded_invoice = self.builder_manager.build_type_b_invoice(
            transaction=self.dummy_transaction,
            invoicer_data=self.dummy_invoicer,
            arca_instance=self.mocked_arca_instance
        )

        importe_gravado = self.dummy_transaction['amount']
        importe_excento_iva = 0
        iva_percentage = 0.21
        importe_iva = importe_gravado * iva_percentage
        importe_total = importe_gravado + importe_excento_iva + importe_iva

        self.assertEqual(builded_invoice['CantReg'], 1)
        self.assertEqual(builded_invoice['PtoVta'], 9)
        self.assertEqual(builded_invoice['CbteTipo'], 6)
        self.assertEqual(builded_invoice['Concepto'], 3)
        self.assertEqual(builded_invoice['DocTipo'], 99)
        self.assertEqual(builded_invoice['DocNro'], 0)
        self.assertEqual(builded_invoice['CbteDesde'], 1)
        self.assertEqual(builded_invoice['CbteHasta'], 1)
        self.assertEqual(builded_invoice['CbteFch'], today_formatted)
        self.assertEqual(builded_invoice['FchServDesde'], today_formatted)
        self.assertEqual(builded_invoice['FchServHasta'], today_formatted)
        self.assertEqual(builded_invoice['FchVtoPago'], today_formatted)
        self.assertEqual(builded_invoice['ImpTotal'], importe_total)
        self.assertEqual(builded_invoice['ImpTotConc'], 0)
        self.assertEqual(builded_invoice['ImpNeto'], importe_gravado)
        self.assertEqual(builded_invoice['ImpOpEx'], importe_excento_iva)
        self.assertEqual(builded_invoice['ImpIVA'], importe_iva)
        self.assertEqual(builded_invoice['ImpTrib'], 0)
        self.assertEqual(builded_invoice['MonId'], "PES")
        self.assertEqual(builded_invoice['MonCotiz'], 1)
        self.assertEqual(builded_invoice['Iva'], [{
            'Id': 5, 'BaseImp': 999, 'Importe': importe_iva
        }])

    def test_instance_manager_works_as_singleton_manager(self):
        self.mock_billing_processor = MagicMock()
        self.mock_afip_instance = MagicMock()
        self.mock_billing_processor.return_value = self.mock_afip_instance

        self.instance_manager = InstanceManager(self.mock_billing_processor)

    def test_singleton_instance_creation(self):
        invoicer_data = {
            'arca_secret_key': 'secret_key_123',
            'arca_certify': 'certify_123',
            'cuit': '20-40937847-2'
        }

        instance1 = self.mocked_instance_manager.get_or_create_instance(
            invoicer_data)

        instance2 = self.mocked_instance_manager.get_or_create_instance(
            invoicer_data)

        self.assertIs(instance1, instance2,
                      "Instances are not the same. Singleton pattern is broken.")
