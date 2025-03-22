from sqlalchemy.orm.session import Session
from app.entities.dtos.invoice_payloads_dto import ClientDTO, SellDTO, BillDTO
from sqlalchemy import exc
from app.entities.models.models import Factura, Facturante, Cliente, Venta
from uuid import uuid4
from app.decorators.transactional import transactional


class BillRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_unique_invoicer(self):
        invoicer_instance = self._session.query(Facturante).one_or_none()
        if not invoicer_instance:
            raise exc.NoResultFound("No results found for invoicer_instance")
        return invoicer_instance.__dict__

    def get_or_create_client(self, payload: ClientDTO):
        client_instance = self._session.query(Cliente).filter(
            documento=payload.documento).first()
        if not client_instance:
            client_instance = Cliente(
                id=uuid4(),
                **payload
            )
            self._session.add(client_instance)
        return client_instance

    def create_and_get_sale(self, payload: SellDTO):
        sell_instance = Venta(
            id=uuid4(),
            **payload
        )
        self._session.add(sell_instance)
        return sell_instance

    @transactional
    def create_bill(self, bill_payload: BillDTO, client_payload: ClientDTO, sell_payload: SellDTO):
        invoicer = self.get_unique_invoicer()
        client = self.get_or_create_client(client_payload)
        sale = self.create_and_get_sale(sell_payload)

        bill_instance = Factura(
            id=uuid4(),
            facturante_id=invoicer.id,
            cliente_id=client.id,
            venta_id=sale.id,
            **bill_payload.dict()
        )
        self._session.add(bill_instance)
        self.close_session()

        return bill_instance

    def close_session(self):
        self._session.close()
