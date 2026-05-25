from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import RetiradaStatus
from app.models.mixins import TimestampMixin


class RetiradaEPI(TimestampMixin, Base):
    __tablename__ = "retiradas_epi"
    __table_args__ = (Index("ix_retiradas_epi_data_retirada", "data_retirada"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    colaborador_id: Mapped[int] = mapped_column(ForeignKey("colaboradores.id"), nullable=False, index=True)
    epi_id: Mapped[int] = mapped_column(ForeignKey("epis.id"), nullable=False, index=True)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    data_retirada: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    data_devolucao_prevista: Mapped[date | None] = mapped_column(Date, nullable=True)
    autorizado_por_matricula: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[RetiradaStatus] = mapped_column(Enum(RetiradaStatus), nullable=False, default=RetiradaStatus.ativo)
    assinatura_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    assinatura_arquivo_criptografado: Mapped[str] = mapped_column(String(260), nullable=False)
    ca_numero_entrega: Mapped[str] = mapped_column(String(40), nullable=False)
    ca_validade_entrega: Mapped[date] = mapped_column(Date, nullable=False)
    devolvido_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    colaborador = relationship("Colaborador", back_populates="retiradas")
    epi = relationship("EPI", back_populates="retiradas")
