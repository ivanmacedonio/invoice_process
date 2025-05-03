
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func


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
    numero_cae: Mapped[str] = mapped_column()
    punto_de_venta: Mapped[int] = mapped_column()
    fecha_vencimiento_cae: Mapped[datetime] = mapped_column()
    arca_secret_key: Mapped[str] = mapped_column()
    arca_certify: Mapped[str] = mapped_column()


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
    tipo_comprobante: Mapped[int] = mapped_column()
    num_comprobante: Mapped[int] = mapped_column()
    punto_de_venta: Mapped[int] = mapped_column()
    fecha_factura: Mapped[datetime] = mapped_column(default=func.now())
    payclub_payment_id: Mapped[str] = mapped_column()


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
