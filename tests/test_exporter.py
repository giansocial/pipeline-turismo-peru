import pytest
import pandas as pd
from pathlib import Path
from src.load.exporter import init_db, load_to_db, export_csv


@pytest.fixture
def db(tmp_path):
    conn = init_db(tmp_path / "test.db")
    yield conn
    conn.close()


def _df():
    return pd.DataFrame({
        "pais": ["Chile", "EEUU"],
        "anio": [2023, 2023],
        "mes": [1, 1],
        "arribos": [82000, 50000],
        "crecimiento_yoy": [5.2, None],
    })


def test_init_creates_tables(db):
    cur = db.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {r[0] for r in cur.fetchall()}
    assert "fact_arribos" in tables
    assert "dim_pais" in tables
    assert "dim_tiempo" in tables


def test_load_inserts(db):
    loaded = load_to_db(_df(), db)
    assert loaded == 2


def test_load_upsert(db):
    load_to_db(_df(), db)
    load_to_db(_df(), db)
    cur = db.execute("SELECT COUNT(*) FROM fact_arribos")
    assert cur.fetchone()[0] == 2


def test_export_csv(tmp_path):
    df = _df()
    path = export_csv(df, tmp_path, "test_export")
    assert path.exists()
    loaded = pd.read_csv(path)
    assert len(loaded) == 2
