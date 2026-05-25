import json
from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.epi import EPI
from app.schemas.epi import EPICreate, EPIUpdate


def _sizes_to_json(sizes: list[str] | None) -> str | None:
    return json.dumps(sizes or [], ensure_ascii=False)


def _sizes_from_json(raw: str | None) -> list[str]:
    return json.loads(raw or "[]")


def create_epi(db: Session, data: EPICreate) -> EPI:
    epi = EPI(**data.model_dump(exclude={"tamanhos_disponiveis"}), tamanhos_disponiveis=_sizes_to_json(data.tamanhos_disponiveis))
    db.add(epi)
    db.commit()
    db.refresh(epi)
    return epi


def list_epis(db: Session, include_deleted: bool = False) -> list[EPI]:
    stmt = select(EPI)
    if not include_deleted:
        stmt = stmt.where(EPI.deleted_at.is_(None))
    return list(db.scalars(stmt.order_by(EPI.nome)))


def get_epi(db: Session, epi_id: int) -> EPI:
    epi = db.get(EPI, epi_id)
    if not epi or epi.deleted_at:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro não encontrado")
    return epi


def update_epi(db: Session, epi_id: int, data: EPIUpdate) -> EPI:
    epi = get_epi(db, epi_id)
    values = data.model_dump(exclude_unset=True)
    if "tamanhos_disponiveis" in values:
        epi.tamanhos_disponiveis = _sizes_to_json(values.pop("tamanhos_disponiveis"))
    for key, value in values.items():
        setattr(epi, key, value)
    db.commit()
    db.refresh(epi)
    return epi


def soft_delete_epi(db: Session, epi_id: int) -> None:
    epi = get_epi(db, epi_id)
    from datetime import datetime, UTC

    epi.deleted_at = datetime.now(UTC)
    db.commit()


def ensure_ca_vigente(epi: EPI) -> None:
    if epi.validade_ca < date.today():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="EPI indisponível para retirada")


def ensure_stock(epi: EPI, quantidade: int) -> None:
    if epi.estoque_atual < quantidade:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Estoque insuficiente")


def to_readable_sizes(epi: EPI) -> EPI:
    epi.tamanhos_disponiveis = _sizes_from_json(epi.tamanhos_disponiveis)  # type: ignore[assignment]
    return epi
