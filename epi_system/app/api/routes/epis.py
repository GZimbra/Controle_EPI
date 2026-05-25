from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.epi import EPICreate, EPIRead, EPIUpdate
from app.services import epi_service

router = APIRouter(prefix="/epis", tags=["epis"])


@router.post("", response_model=EPIRead, status_code=status.HTTP_201_CREATED)
def create(payload: EPICreate, db: Session = Depends(get_db)) -> EPIRead:
    return epi_service.create_epi(db, payload)


@router.get("", response_model=list[EPIRead])
def list_all(db: Session = Depends(get_db)) -> list[EPIRead]:
    return epi_service.list_epis(db)


@router.get("/alertas")
def alertas(db: Session = Depends(get_db)) -> dict:
    from datetime import date, timedelta

    hoje = date.today()
    limite = hoje + timedelta(days=30)
    epis = epi_service.list_epis(db)
    vencidos = [epi for epi in epis if epi.validade_ca < hoje]
    vencendo = [epi for epi in epis if hoje <= epi.validade_ca <= limite]
    estoque_critico = [epi for epi in epis if epi.estoque_atual <= epi.estoque_minimo]
    return {
        "ca_vencidos": len(vencidos),
        "ca_vencendo": len(vencendo),
        "estoque_critico": len(estoque_critico),
        "total": len(vencidos) + len(vencendo) + len(estoque_critico),
        "itens": {
            "ca_vencidos": [{"id": epi.id, "nome": epi.nome, "ca_numero": epi.ca_numero, "validade_ca": epi.validade_ca.isoformat()} for epi in vencidos],
            "ca_vencendo": [{"id": epi.id, "nome": epi.nome, "ca_numero": epi.ca_numero, "validade_ca": epi.validade_ca.isoformat()} for epi in vencendo],
            "estoque_critico": [{"id": epi.id, "nome": epi.nome, "estoque_atual": epi.estoque_atual, "estoque_minimo": epi.estoque_minimo} for epi in estoque_critico],
        },
    }


@router.get("/{epi_id}", response_model=EPIRead)
def get(epi_id: int, db: Session = Depends(get_db)) -> EPIRead:
    return epi_service.get_epi(db, epi_id)


@router.patch("/{epi_id}", response_model=EPIRead)
def update(epi_id: int, payload: EPIUpdate, db: Session = Depends(get_db)) -> EPIRead:
    return epi_service.update_epi(db, epi_id, payload)


@router.delete("/{epi_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(epi_id: int, db: Session = Depends(get_db)) -> Response:
    epi_service.soft_delete_epi(db, epi_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
