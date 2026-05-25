from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.colaborador import Colaborador
from app.schemas.colaborador import ColaboradorCreate, ColaboradorRead, ColaboradorUpdate
from app.services import colaborador_service

router = APIRouter(prefix="/colaboradores", tags=["colaboradores"])


@router.post("", response_model=ColaboradorRead, status_code=status.HTTP_201_CREATED)
def create(payload: ColaboradorCreate, db: Session = Depends(get_db)) -> ColaboradorRead:
    return colaborador_service.create_colaborador(db, payload)


@router.get("", response_model=list[ColaboradorRead])
def list_all(db: Session = Depends(get_db)) -> list[ColaboradorRead]:
    return list(db.scalars(select(Colaborador).where(Colaborador.deleted_at.is_(None)).order_by(Colaborador.nome_completo)))


@router.get("/{colaborador_id}", response_model=ColaboradorRead)
def get(colaborador_id: int, db: Session = Depends(get_db)) -> ColaboradorRead:
    return colaborador_service.get_colaborador(db, colaborador_id)


@router.patch("/{colaborador_id}", response_model=ColaboradorRead)
def update(colaborador_id: int, payload: ColaboradorUpdate, db: Session = Depends(get_db)) -> ColaboradorRead:
    return colaborador_service.update_colaborador(db, colaborador_id, payload)


@router.delete("/{colaborador_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(colaborador_id: int, db: Session = Depends(get_db)) -> Response:
    colaborador_service.soft_delete_colaborador(db, colaborador_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
