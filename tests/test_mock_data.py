"""Unit-тесты генератора синтетических OHLCV-данных."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.mock_data import generate_mock_ohlcv

REQUIRED_COLUMNS = ["date", "open", "high", "low", "close", "volume"]


def test_returns_required_columns() -> None:
    assert list(generate_mock_ohlcv(days=50).columns) == REQUIRED_COLUMNS


def test_respects_requested_length() -> None:
    assert len(generate_mock_ohlcv(days=37)) == 37


def test_is_deterministic() -> None:
    pd.testing.assert_frame_equal(generate_mock_ohlcv(days=30), generate_mock_ohlcv(days=30))


def test_ohlc_invariants_hold() -> None:
    """high накрывает и open, и close; low — под обоими."""
    df = generate_mock_ohlcv(days=500)
    body_high = df[["open", "close"]].max(axis=1)
    body_low = df[["open", "close"]].min(axis=1)

    assert (df["high"] >= body_high).all(), "high оказался ниже open/close"
    assert (df["low"] <= body_low).all(), "low оказался выше open/close"
    assert (df["high"] >= df["low"]).all()


def test_prices_and_volume_are_positive() -> None:
    df = generate_mock_ohlcv(days=200)
    for column in ["open", "high", "low", "close"]:
        assert (df[column] > 0).all()
    assert (df["volume"] > 0).all()


def test_dates_are_monotonic() -> None:
    assert generate_mock_ohlcv(days=60)["date"].is_monotonic_increasing


def test_does_not_mutate_global_random_state() -> None:
    """Генератор не должен трогать глобальный ГСЧ numpy."""
    np.random.seed(123)
    expected = np.random.random(5)

    np.random.seed(123)
    generate_mock_ohlcv(days=10)
    actual = np.random.random(5)

    np.testing.assert_array_equal(actual, expected)


def test_non_positive_days_rejected() -> None:
    with pytest.raises(ValueError):
        generate_mock_ohlcv(days=0)
