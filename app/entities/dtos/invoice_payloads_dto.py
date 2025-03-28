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


@dataclass
class BillToPrintDTO:
    fecha_factura: str
    cuit: str
    punto_de_venta: int
    num_comprobante: int
    cae: str
    fecha_vencimiento_cae: str
    direccion_facturante: str
    telefono_facturante: str
    email_facturante: str
    fecha_factura: str
    inicio_actividades: str
    ingresos_brutos: int
    nombre_cliente: str
    direccion_cliente: str
    provincia_cliente: str
    email_cliente: str
    documento_cliente: str
    metodo_pago: str
    tipo_servicio: str
    fecha_inicio_servicios: str
    fecha_fin_servicios: str
    fecha_pago_servicios: str
    concepto: str
    monto_total: float
    monto_iva: float
