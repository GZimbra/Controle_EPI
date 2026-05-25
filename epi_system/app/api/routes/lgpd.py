from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.lgpd import service
from app.schemas.lgpd import CorrecaoTitularRequest, DireitoTitularResponse, TitularRequest
from app.services.colaborador_service import get_by_matricula

router = APIRouter(prefix="/lgpd", tags=["lgpd"], dependencies=[Depends(get_current_user)])


@router.post("/acesso", response_model=DireitoTitularResponse)
def acesso(payload: TitularRequest, db: Session = Depends(get_db)) -> DireitoTitularResponse:
    return DireitoTitularResponse(direito="acesso", status="concluido", timestamp=datetime.now(UTC), dados=service.export_titular(db, payload.matricula))


@router.post("/correcao", response_model=DireitoTitularResponse)
def correcao(payload: CorrecaoTitularRequest, db: Session = Depends(get_db)) -> DireitoTitularResponse:
    c = get_by_matricula(db, payload.matricula)
    for field in ("nome_completo", "cargo", "setor"):
        value = getattr(payload, field)
        if value is not None:
            setattr(c, field, value)
    db.commit()
    return DireitoTitularResponse(direito="correcao", status="concluido", timestamp=datetime.now(UTC))


@router.post("/exclusao", response_model=DireitoTitularResponse)
def exclusao(payload: TitularRequest, db: Session = Depends(get_db)) -> DireitoTitularResponse:
    return DireitoTitularResponse(direito="exclusao", status="concluido", timestamp=datetime.now(UTC), dados=service.request_exclusion(db, payload.matricula))


@router.post("/portabilidade", response_model=DireitoTitularResponse)
def portabilidade(payload: TitularRequest, db: Session = Depends(get_db)) -> DireitoTitularResponse:
    return DireitoTitularResponse(direito="portabilidade", status="concluido", timestamp=datetime.now(UTC), dados=service.export_titular(db, payload.matricula))


@router.post("/revogacao-consentimento", response_model=DireitoTitularResponse)
def revogacao(payload: TitularRequest, db: Session = Depends(get_db)) -> DireitoTitularResponse:
    service.revoke(db, payload.matricula)
    return DireitoTitularResponse(direito="revogacao_consentimento", status="concluido", timestamp=datetime.now(UTC))


@router.get("/compartilhamento", response_model=DireitoTitularResponse)
def compartilhamento() -> DireitoTitularResponse:
    return DireitoTitularResponse(direito="informacao_compartilhamento", status="concluido", timestamp=datetime.now(UTC), dados=service.sharing_info())


@router.post("/oposicao", response_model=DireitoTitularResponse)
def oposicao(payload: TitularRequest) -> DireitoTitularResponse:
    return DireitoTitularResponse(direito="oposicao", status="registrado_para_analise", timestamp=datetime.now(UTC), dados={"matricula": payload.matricula})


@router.get("/revisao-decisao-automatizada", response_model=DireitoTitularResponse)
def revisao() -> DireitoTitularResponse:
    return DireitoTitularResponse(direito="revisao_decisao_automatizada", status="concluido", timestamp=datetime.now(UTC), dados=service.automated_decision_review())


@router.get("/ripd")
def ripd() -> dict:
    return service.generate_ripd_template()


@router.get("/privacidade", include_in_schema=False)
def privacidade() -> dict:
    settings = get_settings()
    return {
        "politica": "Tratamos dados mínimos para controle legal de entrega de EPIs, com CPF pseudonimizado, assinaturas criptografadas, trilha de auditoria e retenção conforme obrigação legal.",
        "versao": settings.privacy_policy_version,
        "dpo": settings.dpo_contact,
        "direitos": service.DIREITOS_ART_18,
    }
