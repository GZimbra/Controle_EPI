from datetime import datetime

from sqlalchemy import DateTime, Enum, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.enums import AuditOperacao


class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    tabela_afetada: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    registro_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    operacao: Mapped[AuditOperacao] = mapped_column(Enum(AuditOperacao), nullable=False)
    campo_alterado: Mapped[str | None] = mapped_column(String(120), nullable=True)
    valor_anterior: Mapped[str | None] = mapped_column(Text, nullable=True)
    valor_novo: Mapped[str | None] = mapped_column(Text, nullable=True)
    usuario_sistema: Mapped[str] = mapped_column(String(120), nullable=False)
    ip_origem: Mapped[str] = mapped_column(String(80), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
