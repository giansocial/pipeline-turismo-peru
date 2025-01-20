import logging
import sqlite3
from pathlib import Path
import pandas as pd

from src.config.settings import DB_PATH

log = logging.getLogger(__name__)

SCHEMA = """
CREATE TABLE IF NOT EXISTS dim_pais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_tiempo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    anio INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    periodo TEXT NOT NULL,
    trimestre INTEGER NOT NULL,
    UNIQUE(anio, mes)
);

CREATE TABLE IF NOT EXISTS fact_arribos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pais_id INTEGER NOT NULL,
    tiempo_id INTEGER NOT NULL,
    arribos INTEGER NOT NULL,
    crecimiento_yoy REAL,
    FOREIGN KEY (pais_id) REFERENCES dim_pais(id),
    FOREIGN KEY (tiempo_id) REFERENCES dim_tiempo(id),
    UNIQUE(pais_id, tiempo_id)
);
"""


def init_db(db_path: Path = None) -> sqlite3.Connection:
    db_path = db_path or DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def _get_or_create(conn, table, col, value):
    cur = conn.execute(f"SELECT id FROM {table} WHERE {col} = ?", (value,))
    row = cur.fetchone()
    if row:
        return row[0]
    conn.execute(f"INSERT INTO {table} ({col}) VALUES (?)", (value,))
    conn.commit()
    return conn.execute(f"SELECT id FROM {table} WHERE {col} = ?", (value,)).fetchone()[0]


def load_to_db(df: pd.DataFrame, conn: sqlite3.Connection = None) -> int:
    own = conn is None
    if own:
        conn = init_db()

    loaded = 0
    for _, row in df.iterrows():
        pais_id = _get_or_create(conn, "dim_pais", "nombre", row["pais"])

        anio, mes = int(row["anio"]), int(row["mes"])
        periodo = f"{anio}-{str(mes).zfill(2)}"
        trimestre = (mes - 1) // 3 + 1

        cur = conn.execute(
            "SELECT id FROM dim_tiempo WHERE anio = ? AND mes = ?", (anio, mes)
        )
        t = cur.fetchone()
        if t:
            tiempo_id = t[0]
        else:
            conn.execute(
                "INSERT INTO dim_tiempo (anio, mes, periodo, trimestre) VALUES (?,?,?,?)",
                (anio, mes, periodo, trimestre),
            )
            conn.commit()
            tiempo_id = conn.execute(
                "SELECT id FROM dim_tiempo WHERE anio = ? AND mes = ?", (anio, mes)
            ).fetchone()[0]

        conn.execute(
            """INSERT OR REPLACE INTO fact_arribos
               (pais_id, tiempo_id, arribos, crecimiento_yoy) VALUES (?,?,?,?)""",
            (pais_id, tiempo_id, int(row["arribos"]), row.get("crecimiento_yoy")),
        )
        loaded += 1

    conn.commit()
    log.info("cargados %d registros al warehouse", loaded)
    if own:
        conn.close()
    return loaded


def export_csv(df: pd.DataFrame, output_dir: Path, name: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / f"{name}.csv"
    df.to_csv(out, index=False)
    log.info("exportado %s (%d filas)", out.name, len(df))
    return out
