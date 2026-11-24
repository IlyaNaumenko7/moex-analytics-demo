"""Unit-тесты загрузчика: сетевой клиент yfinance полностью изолирован моками."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.data_loader import MOEXDataLoader


@pytest.fixture
def raw_yahoo_df() -> pd.DataFrame:
    index = pd.date_range("2024-01-01", periods=3, freq="D", tz="Europe/Moscow", name="Date")
    return pd.DataFrame(
        {
            "Open": [1.0, 2.0, 3.0],
            "High": [2.0, 3.0, 4.0],
            "Low": [0.5, 1.5, 2.5],
            "Close": [1.5, 2.5, 3.5],
            "Volume": [10, 20, 30],
        },
        index=index,
    )


def test_bare_ticker_gets_me_suffix() -> None:
    assert MOEXDataLoader("sber").ticker == "SBER.ME"


def test_ticker_with_dot_is_preserved() -> None:
    assert MOEXDataLoader("gazp.me").ticker == "GAZP.ME"


def test_get_history_normalizes_contract(raw_yahoo_df: pd.DataFrame) -> None:
    fake_ticker = MagicMock()
    fake_ticker.history.return_value = raw_yahoo_df

    with patch("src.data_loader.yf.Ticker", return_value=fake_ticker) as ctor:
        df = MOEXDataLoader("SBER").get_history("2024-01-01", "2024-01-04")

    assert list(df.columns) == ["date", "open", "high", "low", "close", "volume"]
    assert len(df) == 3
    assert df["date"].dt.tz is None
    ctor.assert_called_once_with("SBER.ME")
    assert fake_ticker.history.call_args.kwargs["interval"] == "1d"


def test_empty_response_raises_value_error() -> None:
    fake_ticker = MagicMock()
    fake_ticker.history.return_value = pd.DataFrame()

    with patch("src.data_loader.yf.Ticker", return_value=fake_ticker):
        with pytest.raises(ValueError, match="Нет данных"):
            MOEXDataLoader("SBER").get_history("2024-01-01", "2024-01-04")


def test_network_failure_is_wrapped_with_cause() -> None:
    fake_ticker = MagicMock()
    fake_ticker.history.side_effect = RuntimeError("connection reset")

    with patch("src.data_loader.yf.Ticker", return_value=fake_ticker):
        with pytest.raises(ValueError, match="Ошибка загрузки") as exc_info:
            MOEXDataLoader("SBER").get_history("2024-01-01", "2024-01-04")

    assert isinstance(exc_info.value.__cause__, RuntimeError)
