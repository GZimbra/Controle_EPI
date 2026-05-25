from datetime import date, datetime

import json

from pydantic import BaseModel, Field, field_validator

from app.models.enums import EPICategoria


class EPIBase(BaseModel):
    nome: str = Field(min_length=2, max_length=160)
    ca_numero: str = Field(min_length=3, max_length=40)
    validade_ca: date
    categoria: EPICategoria
    tamanhos_disponiveis: list[str] = []
    estoque_atual: int = Field(ge=0)
    estoque_minimo: int = Field(ge=0)
    fornecedor: str | None = None


class EPICreate(EPIBase):
    pass


class EPIUpdate(BaseModel):
    nome: str | None = None
    validade_ca: date | None = None
    categoria: EPICategoria | None = None
    tamanhos_disponiveis: list[str] | None = None
    estoque_atual: int | None = Field(default=None, ge=0)
    estoque_minimo: int | None = Field(default=None, ge=0)
    fornecedor: str | None = None


class EPIRead(EPIBase):
    id: int
    ca_vigente: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    model_config = {"from_attributes": True}

    @field_validator("tamanhos_disponiveis", mode="before")
    @classmethod
    def parse_sizes(cls, value):
        if isinstance(value, str):
            return json.loads(value or "[]")
        return value
