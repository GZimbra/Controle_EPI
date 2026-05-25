from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import generate_salt, hash_cpf
from app.models.colaborador import Colaborador
from app.schemas.colaborador import ColaboradorCreate, ColaboradorUpdate


def create_colaborador(db: Session, data: ColaboradorCreate) -> Colaborador:
    salt = generate_salt()
    obj = Colaborador(
        matricula=data.matricula,
        nome_completo=data.nome_completo,
        cargo=data.cargo,
        setor=data.setor,
        tamanho_capacete=data.tamanhos.capacete,
        tamanho_luva=data.tamanhos.luva,
        tamanho_bota=data.tamanhos.bota,
        tamanho_camiseta=data.tamanhos.camiseta,
        cpf_hash=hash_cpf(data.cpf, salt),
        cpf_salt=salt,
        consentimento_timestamp=datetime.now(UTC),
        consentimento_versao=data.consentimento.versao,
        consentimento_canal=data.consentimento.canal,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_colaborador(db: Session, colaborador_id: int) -> Colaborador:
    obj = db.get(Colaborador, colaborador_id)
    if not obj or obj.deleted_at:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro não encontrado")
    return obj


def get_by_matricula(db: Session, matricula: str) -> Colaborador:
    obj = db.scalar(select(Colaborador).where(Colaborador.matricula == matricula, Colaborador.deleted_at.is_(None)))
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro não encontrado")
    return obj


def update_colaborador(db: Session, colaborador_id: int, data: ColaboradorUpdate) -> Colaborador:
    obj = get_colaborador(db, colaborador_id)
    values = data.model_dump(exclude_unset=True)
    tamanhos = values.pop("tamanhos", None)
    for key, value in values.items():
        setattr(obj, key, value)
    if tamanhos:
        obj.tamanho_capacete = tamanhos.get("capacete")
        obj.tamanho_luva = tamanhos.get("luva")
        obj.tamanho_bota = tamanhos.get("bota")
        obj.tamanho_camiseta = tamanhos.get("camiseta")
    db.commit()
    db.refresh(obj)
    return obj


def soft_delete_colaborador(db: Session, colaborador_id: int) -> None:
    obj = get_colaborador(db, colaborador_id)
    obj.deleted_at = datetime.now(UTC)
    db.commit()


def revoke_consent(db: Session, matricula: str) -> Colaborador:
    obj = get_by_matricula(db, matricula)
    obj.consentimento_revogado_em = datetime.now(UTC)
    db.commit()
    db.refresh(obj)
    return obj
