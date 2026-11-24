"""Unit-тесты индикаторов: внешняя библиотека ta изолируется моками."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src import indicators


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame({"close": [float(i) for i in range(1, 61)]})


def test_add_sma_delegates_to_ta_with_correct_window(sample_df: pd.DataFrame) -> None:
    fake = pd.Series([0.0] * len(sample_df))
    with patch("src.indicators.ta.trend.sma_indicator", return_value=fake) as mocked:
        result = indicators.add_sma(sample_df.copy(), period=20)

    assert "sma_20" in result.columns
    mocked.assert_called_once()
    assert mocked.call_args.kwargs["window"] == 20


def test_add_rsi_delegates_to_ta(sample_df: pd.DataFrame) -> None:
    fake = pd.Series([50.0] * len(sample_df))
    with patch("src.indicators.ta.momentum.rsi", return_value=fake) as mocked:
        result = indicators.add_rsi(sample_df.copy(), period=14)

    assert "rsi_14" in result.columns
    assert mocked.call_args.kwargs["window"] == 14


def test_add_bollinger_bands_passes_deviation(sample_df: pd.DataFrame) -> None:
    fake_indicator = MagicMock()
    fake_indicator.bollinger_hband.return_value = pd.Series([3.0] * len(sample_df))
    fake_indicator.bollinger_mavg.return_value = pd.Series([2.0] * len(sample_df))
    fake_indicator.bollinger_lband.return_value = pd.Series([1.0] * len(sample_df))

    with patch("src.indicators.ta.volatility.BollingerBands", return_value=fake_indicator) as ctor:
        result = indicators.add_bollinger_bands(sample_df.copy(), period=20, std=2.0)

    assert {"bb_upper", "bb_middle", "bb_lower"} <= set(result.columns)
    assert ctor.call_args.kwargs["window"] == 20
    assert ctor.call_args.kwargs["window_dev"] == 2.0


def test_compute_all_indicators_adds_expected_columns(sample_df: pd.DataFrame) -> None:
    result = indicators.compute_all_indicators(sample_df.copy())
    expected = {"sma_20", "ema_20", "rsi_14", "bb_upper", "bb_middle", "bb_lower"}
    assert expected <= set(result.columns)


def test_indicators_do_not_mutate_input(sample_df: pd.DataFrame) -> None:
    """Чистая функция не должна менять переданный DataFrame."""
    original = sample_df.copy()
    indicators.compute_all_indicators(sample_df)
    pd.testing.assert_frame_equal(sample_df, original)
