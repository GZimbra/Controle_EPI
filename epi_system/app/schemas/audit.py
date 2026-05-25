from datetime import datetime

from pydantic import BaseModel

from app.models.enums import AuditOperacao


class AuditLogRead(BaseModel):
    id: int
    tabela_afetada: str
    registro_id: str
    operacao: AuditOperacao
    campo_alterado: str | None
    valor_anterior: str | None
    valor_novo: str | None
    usuario_sistema: str
    ip_origem: str
    timestamp: datetime

    model_config = {"from_attributes": True}
