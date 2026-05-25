import csv
import io

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.audit_log import AuditLog
from app.schemas.audit import AuditLogRead

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("", response_model=list[AuditLogRead])
def list_logs(db: Session = Depends(get_db), limit: int = 200) -> list[AuditLogRead]:
    stmt = select(AuditLog).order_by(AuditLog.timestamp.desc()).limit(min(limit, 1000))
    return list(db.scalars(stmt))


@router.get("/export.json")
def export_json(db: Session = Depends(get_db)) -> list[AuditLogRead]:
    return list(db.scalars(select(AuditLog).order_by(AuditLog.timestamp)))


@router.get("/export.csv")
def export_csv(db: Session = Depends(get_db)) -> Response:
    rows = db.scalars(select(AuditLog).order_by(AuditLog.timestamp)).all()
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["id", "tabela_afetada", "registro_id", "operacao", "campo_alterado", "valor_anterior", "valor_novo", "usuario_sistema", "ip_origem", "timestamp"])
    for r in rows:
        writer.writerow([r.id, r.tabela_afetada, r.registro_id, r.operacao.value, r.campo_alterado, r.valor_anterior, r.valor_novo, r.usuario_sistema, r.ip_origem, r.timestamp.isoformat()])
    return Response(out.getvalue(), media_type="text/csv")
