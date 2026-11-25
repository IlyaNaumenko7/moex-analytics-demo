"""Проверка контракта: адаптеры взаимозаменяемы, бизнес-логика от них не зависит."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.data_source import OHLCV_COLUMNS, OHLCVDataSource
from src.indicators import compute_all_indicators
from src.mock_data import generate_mock_ohlcv
from src.sources import CsvSource, MockSource, YahooSource


def test_mock_source_satisfies_contract() -> None:
    assert list(MockSource(days=40).load().columns) == OHLCV_COLUMNS


def test_yahoo_source_satisfies_same_contract() -> None:
    fake_loader = MagicMock()
    fake_loader.get_history.return_value = generate_mock_ohlcv(days=40)

    with patch("src.sources.MOEXDataLoader", return_value=fake_loader):
        source = YahooSource("SBER", "2024-01-01", "2024-02-01")
        assert list(source.load().columns) == OHLCV_COLUMNS

    fake_loader.get_history.assert_called_once_with(
        start_date="2024-01-01", end_date="2024-02-01", interval="1d"
    )


def test_business_logic_is_agnostic_to_source() -> None:
    """Индикаторы считаются одинаково независимо от источника данных."""
    fake_loader = MagicMock()
    fake_loader.get_history.return_value = generate_mock_ohlcv(days=60)

    with patch("src.sources.MOEXDataLoader", return_value=fake_loader):
        sources: list[OHLCVDataSource] = [
            MockSource(days=60),
            YahooSource("SBER", "2024-01-01", "2024-03-01"),
        ]
        for source in sources:
            result = compute_all_indicators(source.load())
            assert {"sma_20", "ema_20", "rsi_14"} <= set(result.columns)


def test_csv_source_satisfies_contract(tmp_path: Path) -> None:
    csv_path = tmp_path / "data.csv"
    generate_mock_ohlcv(days=30).to_csv(csv_path, index=False)

    df = CsvSource(csv_path).load()

    assert list(df.columns) == OHLCV_COLUMNS
    assert len(df) == 30
    assert df["date"].is_monotonic_increasing


def test_csv_source_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="CSV-файл не найден"):
        CsvSource(tmp_path / "absent.csv").load()


def test_csv_source_rejects_incomplete_columns(tmp_path: Path) -> None:
    csv_path = tmp_path / "broken.csv"
    csv_path.write_text("date,open,close\n2024-01-01,1,2\n", encoding="utf-8")

    with pytest.raises(ValueError, match="отсутствуют обязательные колонки"):
        CsvSource(csv_path).load()


def test_all_three_sources_are_interchangeable(tmp_path: Path) -> None:
    """Все три адаптера соответствуют Protocol и отдают одинаковый контракт."""
    csv_path = tmp_path / "data.csv"
    generate_mock_ohlcv(days=60).to_csv(csv_path, index=False)

    fake_loader = MagicMock()
    fake_loader.get_history.return_value = generate_mock_ohlcv(days=60)

    with patch("src.sources.MOEXDataLoader", return_value=fake_loader):
        sources: list[OHLCVDataSource] = [
            MockSource(days=60),
            YahooSource("SBER", "2024-01-01", "2024-03-01"),
            CsvSource(csv_path),
        ]
        for source in sources:
            assert list(source.load().columns) == OHLCV_COLUMNS
