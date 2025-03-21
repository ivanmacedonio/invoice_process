
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func


class Base(DeclarativeBase):
    pass


class Factura(Base):
    __tablename__ = "facturas"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4())
    facturante_id = mapped_column(ForeignKey("facturantes.id"))
    facturante = relationship(
        "Facturante", uselist=False, back_populates="facturas")
    cliente_id = mapped_column(ForeignKey("clientes.id"))
    cliente = relationship("Cliente", uselist=False,
                           back_populates="facturas")
    venta = relationship("Venta", uselist=False, back_populates="factura")
    cae_id = mapped_column(ForeignKey("caes.id"))
    cae = relationship("Cae", uselist=False, back_populates="facturas")
    tipo_comprobante: Mapped[int] = mapped_column()
    num_comprobante: Mapped[int] = mapped_column()
    punto_de_venta: Mapped[int] = mapped_column()
    fecha_factura: Mapped[datetime] = mapped_column(default=func.now())
    payclub_payment_id: Mapped[str] = mapped_column()
