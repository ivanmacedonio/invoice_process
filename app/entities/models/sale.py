
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class Venta(Base):
    __tablename__ = "ventas"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4())
    factura_id = mapped_column(ForeignKey("facturas.id"))
    factura = relationship("Factura", uselist=False, back_populates="venta")
    inicio_servicios: Mapped[datetime] = mapped_column()
    fin_servicios: Mapped[datetime] = mapped_column()
    fecha_de_pago: Mapped[datetime] = mapped_column()
    importe_total: Mapped[int] = mapped_column()
    importe_neto: Mapped[int] = mapped_column()
    importe_iva: Mapped[int] = mapped_column()
