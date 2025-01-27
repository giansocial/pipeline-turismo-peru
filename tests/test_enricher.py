import pytest
import pandas as pd
import numpy as np
from src.transform.enricher import (
    add_yoy_growth, seasonal_index, market_share, covid_impact, recovery_index,
)


def _arrivals_df():
    rows = []
    for anio in [2018, 2019, 2020, 2021, 2022, 2023]:
        for mes in [1, 6, 12]:
            base = 50000 if anio not in (2020, 2021) else 10000
            rows.append({
                "pais": "Estados Unidos",
                "anio": anio, "mes": mes,
                "arribos": base + np.random.randint(-5000, 5000),
            })
            rows.append({
                "pais": "Chile",
                "anio": anio, "mes": mes,
                "arribos": base + np.random.randint(-3000, 3000),
            })
    return pd.DataFrame(rows)


def test_yoy_growth_column():
    df = _arrivals_df()
    result = add_yoy_growth(df)
    assert "crecimiento_yoy" in result.columns


def test_yoy_first_year_null():
    df = _arrivals_df()
    result = add_yoy_growth(df)
    first = result[result["anio"] == 2018]
    assert first["crecimiento_yoy"].isna().all()


def test_seasonal_index():
    df = _arrivals_df()
    seasonal = seasonal_index(df)
    assert "indice_estacional" in seasonal.columns
    assert len(seasonal) > 0


def test_market_share():
    df = _arrivals_df()
    shares = market_share(df)
    assert "participacion_pct" in shares.columns
    for anio in shares["anio"].unique():
        year_total = shares[shares["anio"] == anio]["participacion_pct"].sum()
        assert abs(year_total - 100) < 0.1


def test_covid_impact():
    df = _arrivals_df()
    impact = covid_impact(df)
    assert "caida_pct" in impact.columns
    assert not impact.empty


def test_covid_impact_negative():
    df = _arrivals_df()
    impact = covid_impact(df)
    for _, row in impact.iterrows():
        if not pd.isna(row["caida_pct"]):
            assert row["caida_pct"] < 0


def test_recovery_index():
    df = _arrivals_df()
    rec = recovery_index(df, base_year=2019)
    assert "recuperacion_pct" in rec.columns
    assert rec[rec["anio"] == 2023]["recuperacion_pct"].mean() > 0
