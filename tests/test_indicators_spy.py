"""Проверка делегирования в библиотеку ta через pytest-mock.

mocker.spy оборачивает реальную функцию: вызов записывается, но вычисление
выполняется по-настоящему. Это позволяет проверить и контракт вызова,
и корректность результата — без подмены логики заглушкой.
"""

from __future__ import annotations

import pandas as pd
import pytest
import ta
from pytest_mock import MockerFixture

from src import indicators


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame({"close": [float(i) for i in range(1, 61)]})


def test_add_sma_delegates_to_ta_and_keeps_real_result(
    mocker: MockerFixture, sample_df: pd.DataFrame
) -> None:
    spy = mocker.spy(ta.trend, "sma_indicator")

    result = indicators.add_sma(sample_df, period=20)

    spy.assert_called_once()
    assert spy.call_args is not None
    assert spy.call_args.kwargs["window"] == 20

    # Реальное вычисление не подменено: SMA(20) по значениям 41..60 = 50.5
    assert result["sma_20"].iloc[-1] == pytest.approx(50.5)


def test_add_rsi_passes_window_to_ta(mocker: MockerFixture, sample_df: pd.DataFrame) -> None:
    spy = mocker.spy(ta.momentum, "rsi")

    result = indicators.add_rsi(sample_df, period=14)

    spy.assert_called_once()
    assert spy.call_args is not None
    assert spy.call_args.kwargs["window"] == 14
    assert "rsi_14" in result.columns


def test_bollinger_constructor_receives_deviation(
    mocker: MockerFixture, sample_df: pd.DataFrame
) -> None:
    fake_indicator = mocker.Mock()
    fake_indicator.bollinger_hband.return_value = pd.Series([3.0] * len(sample_df))
    fake_indicator.bollinger_mavg.return_value = pd.Series([2.0] * len(sample_df))
    fake_indicator.bollinger_lband.return_value = pd.Series([1.0] * len(sample_df))

    ctor = mocker.patch("src.indicators.ta.volatility.BollingerBands", return_value=fake_indicator)

    result = indicators.add_bollinger_bands(sample_df, period=20, std=2.0)

    assert {"bb_upper", "bb_middle", "bb_lower"} <= set(result.columns)
    assert ctor.call_args is not None
    assert ctor.call_args.kwargs["window"] == 20
    assert ctor.call_args.kwargs["window_dev"] == 2.0
