import csv
import logging
from pathlib import Path

log = logging.getLogger(__name__)


def load_csv(filepath: Path) -> list[dict]:
    if not filepath.exists():
        raise FileNotFoundError(f"no existe: {filepath}")
    rows = []
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    log.info("cargadas %d filas de %s", len(rows), filepath.name)
    return rows


def load_directory(raw_dir: Path) -> list[dict]:
    all_rows = []
    csv_files = sorted(raw_dir.glob("*.csv"))
    if not csv_files:
        log.warning("sin CSVs en %s", raw_dir)
        return []
    for f in csv_files:
        rows = load_csv(f)
        all_rows.extend(rows)
    log.info("total filas cargadas: %d", len(all_rows))
    return all_rows


def validate_arrivals(rows: list[dict]) -> dict:
    required = {"anio", "mes", "pais", "arribos"}
    if not rows:
        return {"valid": False, "missing_cols": list(required)}
    present = set(rows[0].keys())
    missing = required - present
    return {
        "valid": len(missing) == 0,
        "missing_cols": sorted(missing),
        "total_rows": len(rows),
    }
