from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = PROJECT_ROOT / "epi_system"
sys.path.insert(0, str(APP_ROOT))

from app.main import app

