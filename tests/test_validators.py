import pytest
import pandas as pd
from src.quality.validators import (
    check_completeness, check_uniqueness, check_temporal_coverage, run_quality_report,
)


def _df():
    return pd.DataFrame({
        "pais": ["Chile", "Chile", "EEUU"],
        "anio": [2022, 2023, 2023],
        "mes": [1, 1, 1],
        "arribos": [80000, 82000, 50000],
    })


def test_completeness_full():
    result = check_completeness(_df(), ["pais", "anio", "arribos"])
    assert result["score"] == 100.0


def test_completeness_nulls():
    df = _df()
    df.loc[0, "arribos"] = None
    result = check_completeness(df, ["arribos"])
    assert result["score"] < 100


def test_uniqueness():
    result = check_uniqueness(_df(), ["pais", "anio", "mes"])
    assert result["duplicados"] == 0


def test_temporal_coverage_full():
    df = pd.DataFrame({"anio": [2022, 2023]})
    result = check_temporal_coverage(df, 2022, 2023)
    assert result["score"] == 100.0


def test_temporal_coverage_gap():
    df = pd.DataFrame({"anio": [2022, 2023]})
    result = check_temporal_coverage(df, 2020, 2023)
    assert 2020 in result["anios_faltantes"]
    assert 2021 in result["anios_faltantes"]


def test_quality_report():
    report = run_quality_report(_df())
    assert report["score_total"] > 0
    assert "completitud" in report
