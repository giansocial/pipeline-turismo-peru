import logging
import pandas as pd

log = logging.getLogger(__name__)


def clean_arrivals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    col_map = {c: c.strip().lower().replace(" ", "_") for c in df.columns}
    df = df.rename(columns=col_map)

    if "anio" in df.columns:
        df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
        df = df.dropna(subset=["anio"])
        df["anio"] = df["anio"].astype(int)

    if "mes" in df.columns:
        df["mes"] = pd.to_numeric(df["mes"], errors="coerce")
        df = df.dropna(subset=["mes"])
        df["mes"] = df["mes"].astype(int)

    if "arribos" in df.columns:
        df["arribos"] = (
            df["arribos"].astype(str)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df["arribos"] = pd.to_numeric(df["arribos"], errors="coerce")
        df = df.dropna(subset=["arribos"])
        df["arribos"] = df["arribos"].astype(int)

    if "pais" in df.columns:
        df["pais"] = df["pais"].str.strip().str.title()

    before = len(df)
    df = df.drop_duplicates()
    dropped = before - len(df)
    if dropped > 0:
        log.info("eliminados %d duplicados", dropped)

    return df.reset_index(drop=True)


def add_period(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "anio" in df.columns and "mes" in df.columns:
        df["periodo"] = df["anio"].astype(str) + "-" + df["mes"].astype(str).str.zfill(2)
    return df


def filter_valid_countries(df: pd.DataFrame, valid_countries: list[str]) -> pd.DataFrame:
    if "pais" not in df.columns:
        return df
    valid_set = {p.strip().title() for p in valid_countries}
    mask = df["pais"].isin(valid_set)
    filtered = df[mask].reset_index(drop=True)
    excluded = len(df) - len(filtered)
    if excluded > 0:
        log.info("excluidos %d registros de paises no listados", excluded)
    return filtered
