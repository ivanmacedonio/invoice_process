from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class Facturante(Base):
    __tablename__ = "facturantes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4())
    facturas = relationship("Factura", back_populates="facturante")
    cuit: Mapped[str] = mapped_column()
    razon_social: Mapped[str] = mapped_column()
    inicio_actividades: Mapped[datetime] = mapped_column()
    ii_bb: Mapped[int] = mapped_column()
    telefono: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
