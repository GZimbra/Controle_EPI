from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.retirada import RetiradaEPI
from app.schemas.retirada import RetiradaCreate, RetiradaRead, RetiradaStatusUpdate
from app.services import retirada_service

router = APIRouter(prefix="/retiradas", tags=["retiradas"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=RetiradaRead, status_code=status.HTTP_201_CREATED)
def create(payload: RetiradaCreate, db: Session = Depends(get_db)) -> RetiradaRead:
    return retirada_service.criar_retirada(db, payload)


@router.get("", response_model=list[RetiradaRead])
def list_all(db: Session = Depends(get_db)) -> list[RetiradaRead]:
    return list(db.scalars(select(RetiradaEPI).where(RetiradaEPI.deleted_at.is_(None)).order_by(RetiradaEPI.data_retirada.desc())))


@router.patch("/{retirada_id}/status", response_model=RetiradaRead)
def update_status(retirada_id: int, payload: RetiradaStatusUpdate, db: Session = Depends(get_db)) -> RetiradaRead:
    return retirada_service.atualizar_status(db, retirada_id, payload.status)
