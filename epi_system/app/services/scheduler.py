from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.epi import EPI
from app.services.backup_service import run_backup


def check_ca_and_stock() -> None:
    with SessionLocal() as db:
        epis = db.scalars(select(EPI).where(EPI.deleted_at.is_(None))).all()
        for epi in epis:
            if not epi.ca_vigente or epi.estoque_atual <= epi.estoque_minimo:
                # Produção: enviar alerta para SESMT/segurança por e-mail/SIEM.
                pass


def build_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler(timezone="America/Sao_Paulo")
    scheduler.add_job(check_ca_and_stock, "cron", hour=7, minute=0, id="ca_stock_daily", replace_existing=True)
    scheduler.add_job(run_backup, "cron", hour=2, minute=0, id="backup_daily", replace_existing=True)
    return scheduler
