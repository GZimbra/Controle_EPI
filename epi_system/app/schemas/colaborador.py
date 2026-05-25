from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import ConsentimentoCanal


class TamanhosColaborador(BaseModel):
    capacete: str | None = None
    luva: str | None = None
    bota: str | None = None
    camiseta: str | None = None


class ConsentimentoInput(BaseModel):
    versao: str
    canal: ConsentimentoCanal


class ColaboradorCreate(BaseModel):
    matricula: str = Field(min_length=1, max_length=50)
    nome_completo: str = Field(min_length=3, max_length=180)
    cargo: str = Field(min_length=2, max_length=120)
    setor: str = Field(min_length=2, max_length=120)
    cpf: str = Field(min_length=11, max_length=14)
    tamanhos: TamanhosColaborador = TamanhosColaborador()
    consentimento: ConsentimentoInput


class ColaboradorUpdate(BaseModel):
    nome_completo: str | None = None
    cargo: str | None = None
    setor: str | None = None
    tamanhos: TamanhosColaborador | None = None


class ColaboradorRead(BaseModel):
    id: int
    matricula: str
    nome_completo: str
    cargo: str
    setor: str
    tamanho_capacete: str | None
    tamanho_luva: str | None
    tamanho_bota: str | None
    tamanho_camiseta: str | None
    consentimento_timestamp: datetime
    consentimento_versao: str
    consentimento_canal: ConsentimentoCanal
    consentimento_revogado_em: datetime | None
    deleted_at: datetime | None

    model_config = {"from_attributes": True}
