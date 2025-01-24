import pytest
import pandas as pd
from src.transform.cleaner import clean_arrivals, add_period, filter_valid_countries


def test_clean_normalizes_pais():
    df = pd.DataFrame({
        "pais": [" estados unidos ", "CHILE"],
        "anio": [2023, 2023],
        "mes": [1, 2],
        "arribos": ["50200", "82100"],
    })
    result = clean_arrivals(df)
    assert result["pais"].iloc[0] == "Estados Unidos"
    assert result["pais"].iloc[1] == "Chile"


def test_clean_parses_commas():
    df = pd.DataFrame({
        "pais": ["Chile"],
        "anio": [2023],
        "mes": [1],
        "arribos": ["82,100"],
    })
    result = clean_arrivals(df)
    assert result["arribos"].iloc[0] == 82100


def test_clean_drops_invalid_arribos():
    df = pd.DataFrame({
        "pais": ["Chile", "Chile"],
        "anio": [2023, 2023],
        "mes": [1, 2],
        "arribos": ["82100", "abc"],
    })
    result = clean_arrivals(df)
    assert len(result) == 1


def test_clean_removes_dupes():
    df = pd.DataFrame({
        "pais": ["Chile", "Chile"],
        "anio": [2023, 2023],
        "mes": [1, 1],
        "arribos": ["82100", "82100"],
    })
    result = clean_arrivals(df)
    assert len(result) == 1


def test_add_period():
    df = pd.DataFrame({"anio": [2023], "mes": [3]})
    result = add_period(df)
    assert result["periodo"].iloc[0] == "2023-03"


def test_filter_countries():
    df = pd.DataFrame({
        "pais": ["Chile", "Japon", "Narnia"],
        "arribos": [100, 200, 300],
    })
    result = filter_valid_countries(df, ["Chile", "Japon"])
    assert len(result) == 2


def test_filter_empty_list():
    df = pd.DataFrame({"pais": ["Chile"], "arribos": [100]})
    result = filter_valid_countries(df, [])
    assert len(result) == 0
