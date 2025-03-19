
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.types import Uuid, BigInteger, DateTime


class Base(DeclarativeBase):
    pass


class Venta(Base):
    __tablename__ = "ventas"

    id: Mapped[Uuid] = mapped_column(primary_key=True)
    factura_id = mapped_column(ForeignKey("facturas.id"))
    factura = relationship("Factura", uselist=False, back_populates="venta")
    inicio_servicios: Mapped[DateTime] = mapped_column()
    fin_servicios: Mapped[DateTime] = mapped_column()
    fecha_de_pago: Mapped[DateTime] = mapped_column()
    importe_total: Mapped[BigInteger] = mapped_column()
    importe_neto: Mapped[BigInteger] = mapped_column()
    importe_iva: Mapped[BigInteger] = mapped_column()
