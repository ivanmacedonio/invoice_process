from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime, Uuid, String, Integer


class Base(DeclarativeBase):
    pass


class Facturante(Base):
    __tablename__ = "facturantes"

    id: Mapped[Uuid] = mapped_column(primary_key=True)
    facturas = relationship("Factura", back_populates="facturante")
    cuit: Mapped[String] = mapped_column()
    razon_social: Mapped[String] = mapped_column()
    inicio_actividades: Mapped[DateTime] = mapped_column()
    ii_bb: Mapped[Integer] = mapped_column()
    telefono: Mapped[String] = mapped_column()
    email: Mapped[String] = mapped_column()
