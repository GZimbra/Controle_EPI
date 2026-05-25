from datetime import datetime
from typing import Any

from pydantic import BaseModel


class TitularRequest(BaseModel):
    matricula: str


class CorrecaoTitularRequest(BaseModel):
    matricula: str
    nome_completo: str | None = None
    cargo: str | None = None
    setor: str | None = None


class DireitoTitularResponse(BaseModel):
    direito: str
    status: str
    timestamp: datetime
    dados: dict[str, Any] | None = None
