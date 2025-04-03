from unittest import TestCase
from app.repositories.bill_repository import BillRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.entities.models.models import Facturante, Base
from app.entities.dtos.invoice_payloads_dto import ClientDTO, SellDTO, BillDTO
from datetime import datetime


class TestBillRepository(TestCase):

    def create_engine(self):
        self.engine = create_engine('sqlite:///memory:')

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        self.session = session

    def setup_migrations(self):
        Base.metadata.create_all(self.engine)

    def setup_invoicer_document(self):
        payload: dict = {
            "cuit": "mocked_cuit",
            "razon_social": "mocked_razon_social",
            "inicio_actividades": datetime.now(),
            "ii_bb": 123,
            "telefono": "mocked_phone",
            "email": "test@test.com",
            "numero_cae": "test_numero_cae",
            "punto_de_venta": 123,
            "fecha_vencimiento_cae": datetime.now(),
            "arca_secret_key": "mocked_secret_key",
            "arca_certify": "mocked_arca_certify"
        }
        self.session.add(Facturante(**payload))
        self.session.commit()

    def setup_client_document(self):
        payload = ClientDTO(
            documento="123456",
            codigo_postal="123",
            documento_tipo="dni",
            domicilio="test",
            email="test@test.com",
            provincia="test",
            nombre_completo="test"
        )
        self.client_payload = payload

    def setup_sell_document(self):
        self.sell_payload = SellDTO(
            fecha_de_pago=datetime.now(),
            fin_servicios=datetime.now(),
            importe_iva=12,
            importe_neto=12,
            importe_total=12,
            inicio_servicios=datetime.now()
        )

    def setup_repository(self):
        self.repository = BillRepository(session=self.session)

    def drop_migration(self):
        Base.metadata.drop_all(bind=self.engine)

    def setUp(self):
        self.create_engine()
        self.create_session()
        self.setup_migrations()
        self.setup_client_document()
        self.setup_invoicer_document()
        self.setup_sell_document()
        self.setup_repository()

    def test_get_unique_invoicer_works_successfully(self):
        invoicer_instance = self.repository.get_unique_invoicer()

        self.assertIsNotNone(invoicer_instance)
        self.assertIsInstance(invoicer_instance, dict)
        self.assertIsNotNone(invoicer_instance['cuit'])
        self.assertIsNotNone(invoicer_instance['razon_social'])
        self.assertIsNotNone(invoicer_instance['inicio_actividades'])
        self.assertIsNotNone(invoicer_instance['ii_bb'])
        self.assertIsNotNone(invoicer_instance['telefono'])
        self.assertIsNotNone(invoicer_instance['numero_cae'])
        self.assertIsNotNone(invoicer_instance['punto_de_venta'])
        self.assertIsNotNone(invoicer_instance['fecha_vencimiento_cae'])
        self.assertIsNotNone(invoicer_instance['arca_secret_key'])
        self.assertIsNotNone(invoicer_instance['arca_certify'])

    def test_get_or_create_client_works_successfully(self):
        client_instance = self.repository.get_or_create_client(
            payload=self.client_payload)

        self.assertIsNotNone(client_instance)
        self.assertTrue(isinstance(client_instance, dict))
        self.assertIsNotNone(client_instance['id'])
        self.assertIsNotNone(client_instance['nombre_completo'])
        self.assertIsNotNone(client_instance['email'])
        self.assertIsNotNone(client_instance['documento'])
        self.assertIsNotNone(client_instance['documento_tipo'])
        self.assertIsNotNone(client_instance['provincia'])
        self.assertIsNotNone(client_instance['domicilio'])
        self.assertIsNotNone(client_instance['codigo_postal'])

    def test_create_sale_works_successfully(self):
        invoicer_instance = self.repository.get_unique_invoicer()

        sell_instance = self.repository.create_and_get_sale(
            invoice_id=invoicer_instance['id'],
            payload=self.sell_payload
        )

        self.assertIsNotNone(sell_instance)
        self.assertIsNotNone(sell_instance['factura_id'])
        self.assertIsNotNone(sell_instance['inicio_servicios'])
        self.assertIsNotNone(sell_instance['fin_servicios'])
        self.assertIsNotNone(sell_instance['fecha_de_pago'])
        self.assertIsNotNone(sell_instance['importe_total'])
        self.assertIsNotNone(sell_instance['importe_neto'])
        self.assertIsNotNone(sell_instance['importe_iva'])

    def test_create_bill_transaction(self):
        bill_payload = BillDTO(
            fecha_factura=datetime.now(),
            num_comprobante=1,
            tipo_comprobante=1,
            payclub_payment_id="test_id",
            punto_de_venta=123
        )
        bill_instance = self.repository.create_bill(
            sell_payload=self.sell_payload,
            client_payload=self.client_payload,
            bill_payload=bill_payload
        )

        self.assertIsNotNone(bill_instance)
        self.assertIsNotNone(bill_instance['facturante_id'])
        self.assertIsNotNone(bill_instance['cliente_id'])
        self.assertIsNotNone(bill_instance['num_comprobante'])
        self.assertIsNotNone(bill_instance['tipo_comprobante'])
        self.assertIsNotNone(bill_instance['punto_de_venta'])
        self.assertIsNotNone(bill_instance['fecha_factura'])
        self.assertIsNotNone(bill_instance['payclub_payment_id'])

    def tearDown(self):
        self.drop_migration()
