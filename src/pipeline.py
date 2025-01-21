import argparse
import json
import logging
import time

import pandas as pd

from src.config.settings import RAW_DIR, PROCESSED_DIR, PAISES_TOP
from src.extract.data_loader import load_directory
from src.transform.cleaner import clean_arrivals, add_period, filter_valid_countries
from src.transform.enricher import (
    add_yoy_growth, seasonal_index, market_share,
    covid_impact, recovery_index,
)
from src.quality.validators import run_quality_report
from src.load.exporter import init_db, load_to_db, export_csv
from src.utils.logger import setup_logging

log = logging.getLogger(__name__)


def run_pipeline(raw_dir=None, countries: list[str] = None) -> dict:
    t0 = time.time()
    raw_dir = raw_dir or RAW_DIR

    rows = load_directory(raw_dir)
    if not rows:
        log.error("sin datos")
        return {"error": "sin datos"}

    df = pd.DataFrame(rows)
    df = clean_arrivals(df)
    df = add_period(df)

    if countries:
        df = filter_valid_countries(df, countries)

    quality = run_quality_report(df)
    log.info("calidad: %.1f%%", quality["score_total"])

    df = add_yoy_growth(df)

    conn = init_db()
    loaded = load_to_db(df, conn)
    conn.close()

    export_csv(df, PROCESSED_DIR, "arribos_enriquecidos")

    shares = market_share(df)
    export_csv(shares, PROCESSED_DIR, "participacion_mercado")

    seasonal = seasonal_index(df)
    export_csv(seasonal, PROCESSED_DIR, "indice_estacional")

    if 2020 in df["anio"].values:
        impact = covid_impact(df)
        export_csv(impact, PROCESSED_DIR, "impacto_covid")

        rec = recovery_index(df, base_year=2019)
        export_csv(rec, PROCESSED_DIR, "recuperacion_post_covid")

    elapsed = round(time.time() - t0, 1)
    log.info("pipeline completado en %.1fs", elapsed)

    return {
        "filas_procesadas": len(df),
        "filas_cargadas": loaded,
        "calidad_pct": quality["score_total"],
        "paises": sorted(df["pais"].unique().tolist()),
        "duracion_seg": elapsed,
    }


def main():
    parser = argparse.ArgumentParser(description="Pipeline turismo Peru - MINCETUR")
    parser.add_argument("--countries", nargs="+", help="filtrar por paises")
    args = parser.parse_args()

    setup_logging()
    result = run_pipeline(countries=args.countries)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
