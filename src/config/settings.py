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

MINCETUR_STATS_URL = (
    "https://www.mincetur.gob.pe/turismo/estadisticas-generales/"
)
DATATUR_URL = "https://dataturismo.mincetur.gob.pe/"

PAISES_TOP = [
    "Estados Unidos", "Chile", "Ecuador", "Colombia", "Argentina",
    "Brasil", "Espana", "Francia", "Alemania", "Reino Unido",
    "Mexico", "Canada", "Bolivia", "Japon", "Italia",
]

PUNTOS_ENTRADA = [
    "Aeropuerto Jorge Chavez",
    "Santa Rosa (Tacna)",
    "Desaguadero (Puno)",
    "Aguas Verdes (Tumbes)",
    "Aeropuerto Cusco",
    "Puerto del Callao",
]

REGIONES = [
    "Lima", "Cusco", "Arequipa", "Puno", "Tacna",
    "Piura", "La Libertad", "Lambayeque", "Ica", "Junin",
    "Loreto", "Madre de Dios", "Ancash", "Cajamarca", "San Martin",
]

ANIO_INICIO = 2015
ANIO_FIN = 2023

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
