
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func
from sqlalchemy.types import DateTime, Uuid, String, BigInteger
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Factura(Base):
    __tablename__ = "facturas"

    id: Mapped[Uuid] = mapped_column(primary_key=True)
    facturante_id = mapped_column(ForeignKey("facturantes.id"))
    facturante = relationship(
        "Facturante", uselist=False, back_populates="facturas")
    cliente_id = mapped_column(ForeignKey("clientes.id"))
    cliente = relationship("Cliente", uselist=False,
                           back_populates="facturas")
    venta = relationship("Venta", uselist=False, back_populates="factura")
    cae_id = mapped_column(ForeignKey("caes.id"))
    cae = relationship("Cae", uselist=False, back_populates="facturas")
    tipo_comprobante: Mapped[BigInteger] = mapped_column()
    num_comprobante: Mapped[BigInteger] = mapped_column()
    punto_de_venta: Mapped[BigInteger] = mapped_column()
    fecha_factura: Mapped[DateTime] = mapped_column(default=func.now())
    payclub_payment_id: Mapped[String] = mapped_column()
