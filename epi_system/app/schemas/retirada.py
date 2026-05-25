from datetime import date, datetime

from pydantic import BaseModel, Field

from app.models.enums import RetiradaStatus


class RetiradaCreate(BaseModel):
    colaborador_id: int
    epi_id: int
    quantidade: int = Field(gt=0)
    data_devolucao_prevista: date | None = None
    autorizado_por_matricula: str = Field(min_length=1, max_length=50)
    assinatura_base64: str = Field(min_length=32)


class RetiradaStatusUpdate(BaseModel):
    status: RetiradaStatus


class RetiradaRead(BaseModel):
    id: int
    colaborador_id: int
    epi_id: int
    quantidade: int
    data_retirada: datetime
    data_devolucao_prevista: date | None
    autorizado_por_matricula: str
    status: RetiradaStatus
    assinatura_hash: str
    assinatura_arquivo_criptografado: str
    ca_numero_entrega: str
    ca_validade_entrega: date
    devolvido_em: datetime | None

    model_config = {"from_attributes": True}
