
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid, String
from typing import List


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "clientes"

    id: Mapped[Uuid] = mapped_column(primary_key=True)
    nombre: Mapped[String] = mapped_column()
    apellido: Mapped[String] = mapped_column()
    email: Mapped[String] = mapped_column()
    documento: Mapped[String] = mapped_column()
    documento_tipo: Mapped[String] = mapped_column()
    facturas = relationship("Factura", back_populates="cliente")
