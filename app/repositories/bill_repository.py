from sqlalchemy.orm.session import Session
from app.configs.logger import logger
from app.entities.dtos.invoice_payloads_dto import ClientDTO, SellDTO, BillDTO
from sqlalchemy import exc
from app.entities.models.models import Factura, Facturante, Cliente, Venta
from uuid import uuid4
from app.decorators.transactional import transactional
from app.interfaces.bill_repository_interface import IBillRepository


class BillRepository(IBillRepository):
    def __init__(self, session: Session):
        self._session = session

    def bill_was_already_invoiced(self, txid):
        return self._session.query(Factura).filter_by(payclub_payment_id=txid).count() > 0

    def get_unique_invoicer(self):
        invoicer_instance = self._session.query(Facturante).one_or_none()
        if not invoicer_instance:
            raise exc.NoResultFound("No results found for invoicer_instance")
        return invoicer_instance.__dict__

    def get_or_create_client(self, payload: ClientDTO):
        client_instance = self._session.query(Cliente).filter_by(
            documento=payload.documento).first()
        if not client_instance:
            client_instance = Cliente(
                id=uuid4(),
                **payload.__dict__
            )
            self._session.add(client_instance)
        return client_instance.__dict__

    def create_and_get_sale(self, payload: SellDTO, invoice_id):
        sell_instance = Venta(
            id=uuid4(),
            factura_id=invoice_id,
            **payload.__dict__
        )
        self._session.add(sell_instance)
        return sell_instance.__dict__

    @transactional
    def create_bill(self, bill_payload, client_payload, sell_payload):
        invoicer = self.get_unique_invoicer()
        client = self.get_or_create_client(client_payload)

        bill_instance = Factura(
            id=uuid4(),
            facturante_id=invoicer['id'],
            cliente_id=client['id'],
            **bill_payload.__dict__
        )

        self._session.add(bill_instance)

        self.create_and_get_sale(
            payload=sell_payload,
            invoice_id=bill_instance.id)

        logger.info("Bill created successfully")
        return bill_instance.__dict__

    def close_session(self):
        self._session.close()
