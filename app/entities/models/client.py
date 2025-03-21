
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4())
    nombre_completo: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    documento: Mapped[str] = mapped_column()
    documento_tipo: Mapped[str] = mapped_column()
    provincia: Mapped[str] = mapped_column()
    domicilio: Mapped[str] = mapped_column()
    codigo_postal: Mapped[str] = mapped_column()
    facturas = relationship("Factura", back_populates="cliente")
