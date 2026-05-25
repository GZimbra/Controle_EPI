from datetime import datetime

from sqlalchemy import DateTime, Enum, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ConsentimentoCanal
from app.models.mixins import TimestampMixin


class Colaborador(TimestampMixin, Base):
    __tablename__ = "colaboradores"
    __table_args__ = (UniqueConstraint("matricula", name="uq_colaboradores_matricula"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    matricula: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    nome_completo: Mapped[str] = mapped_column(String(180), nullable=False)
    cargo: Mapped[str] = mapped_column(String(120), nullable=False)
    setor: Mapped[str] = mapped_column(String(120), nullable=False)
    tamanho_capacete: Mapped[str | None] = mapped_column(String(20), nullable=True)
    tamanho_luva: Mapped[str | None] = mapped_column(String(20), nullable=True)
    tamanho_bota: Mapped[str | None] = mapped_column(String(20), nullable=True)
    tamanho_camiseta: Mapped[str | None] = mapped_column(String(20), nullable=True)
    cpf_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    cpf_salt: Mapped[str] = mapped_column(String(32), nullable=False)
    consentimento_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    consentimento_versao: Mapped[str] = mapped_column(String(40), nullable=False)
    consentimento_canal: Mapped[ConsentimentoCanal] = mapped_column(Enum(ConsentimentoCanal), nullable=False)
    consentimento_revogado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    retiradas = relationship("RetiradaEPI", back_populates="colaborador")
