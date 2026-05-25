from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import RetiradaStatus
from app.models.retirada import RetiradaEPI
from app.schemas.retirada import RetiradaCreate
from app.services.colaborador_service import get_colaborador
from app.services.epi_service import ensure_ca_vigente, ensure_stock, get_epi
from app.services.signature_service import save_encrypted_signature


def criar_retirada(db: Session, data: RetiradaCreate) -> RetiradaEPI:
    colaborador = get_colaborador(db, data.colaborador_id)
    epi = get_epi(db, data.epi_id)
    ensure_ca_vigente(epi)
    ensure_stock(epi, data.quantidade)
    if colaborador.consentimento_revogado_em:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Operação não permitida")

    assinatura_hash, assinatura_path = save_encrypted_signature(data.assinatura_base64)
    retirada = RetiradaEPI(
        colaborador_id=data.colaborador_id,
        epi_id=data.epi_id,
        quantidade=data.quantidade,
        data_retirada=datetime.now(UTC),
        data_devolucao_prevista=data.data_devolucao_prevista,
        autorizado_por_matricula=data.autorizado_por_matricula,
        status=RetiradaStatus.ativo,
        assinatura_hash=assinatura_hash,
        assinatura_arquivo_criptografado=assinatura_path,
        ca_numero_entrega=epi.ca_numero,
        ca_validade_entrega=epi.validade_ca,
    )
    epi.estoque_atual -= data.quantidade
    db.add(retirada)
    db.commit()
    db.refresh(retirada)
    return retirada


def atualizar_status(db: Session, retirada_id: int, status_value: RetiradaStatus) -> RetiradaEPI:
    retirada = db.get(RetiradaEPI, retirada_id)
    if not retirada or retirada.deleted_at:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro não encontrado")
    if retirada.status == RetiradaStatus.ativo and status_value == RetiradaStatus.devolvido:
        retirada.epi.estoque_atual += retirada.quantidade
        retirada.devolvido_em = datetime.now(UTC)
    retirada.status = status_value
    db.commit()
    db.refresh(retirada)
    return retirada
