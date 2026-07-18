import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
LOG_DIR = BASE_DIR / "logs"

for _d in (RAW_DIR, PROCESSED_DIR, LOG_DIR):
    _d.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "turismo.db"

PAISES_TOP = [
    "Estados Unidos", "Chile", "Ecuador", "Colombia", "Argentina",
    "Brasil", "Espana", "Francia", "Alemania", "Reino Unido",
    "Mexico", "Canada", "Bolivia", "Japon", "Italia",
]

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
