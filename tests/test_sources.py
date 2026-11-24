"""Проверка контракта: адаптеры взаимозаменяемы, бизнес-логика от них не зависит."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.data_source import OHLCV_COLUMNS, OHLCVDataSource
from src.indicators import compute_all_indicators
from src.mock_data import generate_mock_ohlcv
from src.sources import MockSource, YahooSource


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
