from datetime import UTC, datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models.colaborador import Colaborador
from app.services.colaborador_service import get_by_matricula, revoke_consent


DIREITOS_ART_18 = [
    "acesso",
    "correcao",
    "exclusao",
    "portabilidade",
    "revogacao_consentimento",
    "informacao_compartilhamento",
    "oposicao",
    "revisao_decisao_automatizada",
]


def export_titular(db: Session, matricula: str) -> dict[str, Any]:
    c = get_by_matricula(db, matricula)
    return {
        "matricula": c.matricula,
        "nome_completo": c.nome_completo,
        "cargo": c.cargo,
        "setor": c.setor,
        "tamanhos": {
            "capacete": c.tamanho_capacete,
            "luva": c.tamanho_luva,
            "bota": c.tamanho_bota,
            "camiseta": c.tamanho_camiseta,
        },
        "consentimento": {
            "timestamp": c.consentimento_timestamp.isoformat(),
            "versao": c.consentimento_versao,
            "canal": c.consentimento_canal.value,
            "revogado_em": c.consentimento_revogado_em.isoformat() if c.consentimento_revogado_em else None,
        },
        "observacao": "CPF e assinatura não são exportados em claro; armazenados somente como hash/arquivo criptografado.",
    }


def request_exclusion(db: Session, matricula: str) -> dict[str, str]:
    c = get_by_matricula(db, matricula)
    c.deleted_at = datetime.now(UTC)
    db.commit()
    return {"status": "exclusao_logica_executada", "base_legal": "retenção legal preservada por NR-1/LGPD art. 15"}


def sharing_info() -> dict[str, Any]:
    return {
        "compartilhamento": "Dados restritos ao SESMT, segurança do trabalho, RH autorizado e auditorias legais.",
        "terceiros": [],
        "transferencia_internacional": False,
    }


def automated_decision_review() -> dict[str, str]:
    return {"status": "não aplicável", "motivo": "Sistema não executa decisão automatizada com efeito jurídico."}


def generate_ripd_template() -> dict[str, Any]:
    return {
        "titulo": "Relatório de Impacto à Proteção de Dados - Controle de EPI",
        "base_legal": ["cumprimento de obrigação legal/regulatória", "proteção da vida e incolumidade física"],
        "dados_tratados": ["identificação funcional mínima", "tamanhos de EPI", "hash de CPF", "assinatura criptografada"],
        "riscos": ["acesso indevido", "vazamento de metadados", "retenção excessiva"],
        "controles": ["JWT", "criptografia Fernet", "audit trail imutável", "soft delete", "minimização", "backups retidos"],
        "retencao": "Configurável por DATA_RETENTION_YEARS; mínimo operacional recomendado: 5 anos.",
    }


def revoke(db: Session, matricula: str) -> Colaborador:
    return revoke_consent(db, matricula)
