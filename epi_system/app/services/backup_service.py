import shutil
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path

from app.core.config import get_settings


def run_backup() -> Path:
    settings = get_settings()
    backup_dir = Path(settings.backup_dir)
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    database_url = settings.database_url
    if database_url.startswith("sqlite:///"):
        source = Path(database_url.replace("sqlite:///", "", 1))
        target = backup_dir / f"sqlite-{stamp}.db"
        shutil.copy2(source, target)
    else:
        target = backup_dir / f"postgres-{stamp}.dump"
        with target.open("wb") as fh:
            subprocess.run(["pg_dump", database_url], stdout=fh, check=True)
    purge_old_backups()
    return target


def purge_old_backups() -> None:
    settings = get_settings()
    cutoff = datetime.now(UTC) - timedelta(days=settings.backup_retention_years * 365)
    for file in Path(settings.backup_dir).glob("*"):
        if file.is_file() and datetime.fromtimestamp(file.stat().st_mtime, UTC) < cutoff:
            file.unlink()
