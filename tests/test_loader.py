import pytest
from pathlib import Path
from src.extract.data_loader import load_csv, load_directory, validate_arrivals

FIXTURES = Path(__file__).parent / "fixtures"


def test_load_csv():
    rows = load_csv(FIXTURES / "arribos_sample.csv")
    assert len(rows) > 0
    assert "pais" in rows[0]


def test_load_csv_not_found():
    with pytest.raises(FileNotFoundError):
        load_csv(FIXTURES / "nope.csv")


def test_load_directory():
    rows = load_directory(FIXTURES)
    assert len(rows) > 30


def test_load_directory_empty(tmp_path):
    rows = load_directory(tmp_path)
    assert rows == []


def test_validate_ok():
    rows = [{"anio": "2023", "mes": "1", "pais": "Chile", "arribos": "100"}]
    result = validate_arrivals(rows)
    assert result["valid"] is True


def test_validate_missing_col():
    rows = [{"anio": "2023", "mes": "1"}]
    result = validate_arrivals(rows)
    assert result["valid"] is False
    assert "pais" in result["missing_cols"]
