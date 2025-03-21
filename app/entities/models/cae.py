
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class Cae(Base):
    __tablename__ = "caes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4())
    cae: Mapped[str] = mapped_column()
    fecha_vencimiento: Mapped[datetime] = mapped_column()
    facturas = relationship("Facturas", back_populates="cae")
