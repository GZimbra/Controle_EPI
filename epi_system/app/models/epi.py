from datetime import date

from sqlalchemy import Date, Enum, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import EPICategoria
from app.models.mixins import TimestampMixin


class EPI(TimestampMixin, Base):
    __tablename__ = "epis"
    __table_args__ = (UniqueConstraint("ca_numero", name="uq_epis_ca_numero"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(160), nullable=False)
    ca_numero: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    validade_ca: Mapped[date] = mapped_column(Date, nullable=False)
    categoria: Mapped[EPICategoria] = mapped_column(Enum(EPICategoria), nullable=False)
    tamanhos_disponiveis: Mapped[str | None] = mapped_column(Text, nullable=True)
    estoque_atual: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    estoque_minimo: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    fornecedor: Mapped[str | None] = mapped_column(String(160), nullable=True)

    retiradas = relationship("RetiradaEPI", back_populates="epi")

    @property
    def ca_vigente(self) -> bool:
        return self.validade_ca >= date.today()
