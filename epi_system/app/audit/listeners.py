import json
from datetime import date, datetime
from typing import Any

from sqlalchemy import event, inspect
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapper

from app.core.audit_context import audit_ip, audit_user
from app.core.security import sha256_hex
from app.models.audit_log import AuditLog
from app.models.enums import AuditOperacao

SENSITIVE_FIELDS = {
    "nome_completo",
    "cpf_hash",
    "cpf_salt",
    "assinatura_hash",
    "assinatura_arquivo_criptografado",
}


def _safe_value(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (datetime, date)):
        value = value.isoformat()
    if isinstance(value, (dict, list, tuple)):
        value = json.dumps(value, ensure_ascii=False, default=str)
    text = str(value)
    if len(text) > 500:
        text = text[:500]
    return text


def _audit_value(field: str, value: Any) -> str | None:
    if field in SENSITIVE_FIELDS and value is not None:
        return f"sha256:{sha256_hex(str(value))}"
    return _safe_value(value)


def _insert_log(
    connection: Connection,
    table: str,
    record_id: str,
    operation: AuditOperacao,
    field: str | None,
    old: Any,
    new: Any,
) -> None:
    connection.execute(
        AuditLog.__table__.insert().values(
            tabela_afetada=table,
            registro_id=str(record_id),
            operacao=operation,
            campo_alterado=field,
            valor_anterior=_audit_value(field or "", old),
            valor_novo=_audit_value(field or "", new),
            usuario_sistema=audit_user.get(),
            ip_origem=audit_ip.get(),
        )
    )


def after_insert(mapper: Mapper[Any], connection: Connection, target: Any) -> None:
    if isinstance(target, AuditLog):
        return
    _insert_log(connection, target.__tablename__, getattr(target, "id", "unknown"), AuditOperacao.insert, None, None, "created")


def after_update(mapper: Mapper[Any], connection: Connection, target: Any) -> None:
    if isinstance(target, AuditLog):
        return
    state = inspect(target)
    for attr in state.attrs:
        hist = attr.history
        if hist.has_changes():
            old = hist.deleted[0] if hist.deleted else None
            new = hist.added[0] if hist.added else None
            _insert_log(connection, target.__tablename__, getattr(target, "id", "unknown"), AuditOperacao.update, attr.key, old, new)


def after_delete(mapper: Mapper[Any], connection: Connection, target: Any) -> None:
    if isinstance(target, AuditLog):
        return
    _insert_log(connection, target.__tablename__, getattr(target, "id", "unknown"), AuditOperacao.delete, None, "deleted", None)


def block_audit_mutation(mapper: Mapper[Any], connection: Connection, target: AuditLog) -> None:
    raise RuntimeError("audit_log é imutável")


def register_audit_listeners() -> None:
    from app.models.colaborador import Colaborador
    from app.models.epi import EPI
    from app.models.retirada import RetiradaEPI
    from app.models.usuario import UsuarioSistema

    for model in (Colaborador, EPI, RetiradaEPI, UsuarioSistema):
        event.listen(model, "after_insert", after_insert, propagate=True)
        event.listen(model, "after_update", after_update, propagate=True)
        event.listen(model, "after_delete", after_delete, propagate=True)
    event.listen(AuditLog, "before_update", block_audit_mutation, propagate=True)
    event.listen(AuditLog, "before_delete", block_audit_mutation, propagate=True)
