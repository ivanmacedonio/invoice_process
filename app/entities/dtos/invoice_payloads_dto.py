from dataclasses import dataclass
from sqlalchemy.types import UUID, DateTime
from typing import Union


@dataclass
class ClientDTO:
    nombre_completo: str
    email: str
    documento: str
    documento_tipo: str
    provincia: str
    domicilio: str
    codigo_postal: Union[str, int]


@dataclass
class SellDTO:
    inicio_servicios: DateTime
    fin_servicios: DateTime
    fecha_de_pago: DateTime
    importe_total: int
    importe_neto: int
    importe_iva: int


@dataclass
class BillDTO:
    tipo_comprobante: int
    num_comprobante: int
    punto_de_venta: int
    fecha_factura: DateTime
    payclub_payment_id: str
