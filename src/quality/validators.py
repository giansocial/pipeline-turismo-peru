import logging
import pandas as pd

log = logging.getLogger(__name__)


def check_completeness(df: pd.DataFrame, required: list[str]) -> dict:
    total = len(df)
    if total == 0:
        return {"score": 0.0, "detalles": {}}
    detalles = {}
    for col in required:
        if col in df.columns:
            nulls = df[col].isnull().sum()
            detalles[col] = round((1 - nulls / total) * 100, 1)
        else:
            detalles[col] = 0.0
    score = sum(detalles.values()) / len(detalles)
    return {"score": round(score, 1), "detalles": detalles}


def check_uniqueness(df: pd.DataFrame, keys: list[str]) -> dict:
    total = len(df)
    if total == 0:
        return {"score": 100.0, "duplicados": 0}
    dupes = df.duplicated(subset=keys).sum()
    score = (1 - dupes / total) * 100
    return {"score": round(score, 1), "duplicados": int(dupes)}


def check_temporal_coverage(df: pd.DataFrame, start_year: int, end_year: int) -> dict:
    if "anio" not in df.columns:
        return {"score": 0.0, "anios_faltantes": []}
    expected = set(range(start_year, end_year + 1))
    present = set(df["anio"].unique())
    missing = sorted(expected - present)
    score = len(present & expected) / len(expected) * 100 if expected else 0
    return {"score": round(score, 1), "anios_faltantes": missing}


def run_quality_report(df: pd.DataFrame) -> dict:
    required = ["pais", "anio", "mes", "arribos"]
    completeness = check_completeness(df, required)
    uniqueness = check_uniqueness(df, ["pais", "anio", "mes"])
    temporal = check_temporal_coverage(df, 2015, 2023)

    total = (
        completeness["score"] * 0.4
        + uniqueness["score"] * 0.3
        + temporal["score"] * 0.3
    )

    report = {
        "score_total": round(total, 1),
        "completitud": completeness,
        "unicidad": uniqueness,
        "cobertura_temporal": temporal,
        "filas": len(df),
    }
    log.info("calidad: %.1f%% (%d filas)", total, len(df))
    return report
