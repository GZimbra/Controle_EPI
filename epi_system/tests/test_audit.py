from datetime import UTC, datetime

from app.models.audit_log import AuditLog
from app.models.colaborador import Colaborador
from app.models.enums import ConsentimentoCanal


def test_audit_listener_pseudonymizes_personal_field(db):
    c = Colaborador(
        matricula="M1",
        nome_completo="Pessoa Teste",
        cargo="Tec",
        setor="Ops",
        cpf_hash="a" * 64,
        cpf_salt="b" * 32,
        consentimento_timestamp=datetime.now(UTC),
        consentimento_versao="v1",
        consentimento_canal=ConsentimentoCanal.web,
    )
    db.add(c)
    db.commit()
    c.nome_completo = "Pessoa Alterada"
    db.commit()
    logs = db.query(AuditLog).filter(AuditLog.tabela_afetada == "colaboradores").all()
    assert logs
    assert any(log.campo_alterado == "nome_completo" and "Pessoa" not in (log.valor_novo or "") for log in logs)
