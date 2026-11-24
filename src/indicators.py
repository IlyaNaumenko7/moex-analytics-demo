"""Расчёт технических индикаторов.

Все публичные функции чистые: возвращают новый DataFrame и не меняют входной.
Единственная вычислительная зависимость слоя — библиотека ta.
"""

from __future__ import annotations

import pandas as pd
import ta

DEFAULT_SMA_PERIOD = 20
DEFAULT_EMA_PERIOD = 20
DEFAULT_RSI_PERIOD = 14
DEFAULT_BB_PERIOD = 20
DEFAULT_BB_STD = 2.0
PRICE_COLUMN = "close"


def _validate(df: pd.DataFrame, period: int, column: str) -> None:
    """Проверяет предусловия расчёта: непустой набор, валидный период, наличие колонки."""
    if df.empty:
        raise ValueError("DataFrame пуст — расчёт индикаторов невозможен")
    if period <= 0:
        raise ValueError(f"period должен быть положительным, получено {period}")
    if column not in df.columns:
        raise KeyError(f"В DataFrame отсутствует колонка '{column}'")


def _apply_sma(df: pd.DataFrame, period: int, column: str) -> pd.DataFrame:
    df[f"sma_{period}"] = ta.trend.sma_indicator(df[column], window=period)
    return df


def _apply_ema(df: pd.DataFrame, period: int, column: str) -> pd.DataFrame:
    df[f"ema_{period}"] = ta.trend.ema_indicator(df[column], window=period)
    return df


def _apply_rsi(df: pd.DataFrame, period: int, column: str) -> pd.DataFrame:
    df[f"rsi_{period}"] = ta.momentum.rsi(df[column], window=period)
    return df


def _apply_bollinger(df: pd.DataFrame, period: int, std: float, column: str) -> pd.DataFrame:
    indicator = ta.volatility.BollingerBands(close=df[column], window=period, window_dev=std)
    df["bb_upper"] = indicator.bollinger_hband()
    df["bb_middle"] = indicator.bollinger_mavg()
    df["bb_lower"] = indicator.bollinger_lband()
    return df


def add_sma(
    df: pd.DataFrame, period: int = DEFAULT_SMA_PERIOD, column: str = PRICE_COLUMN
) -> pd.DataFrame:
    """Добавляет простую скользящую среднюю (SMA). Входной DataFrame не меняется."""
    _validate(df, period, column)
    return _apply_sma(df.copy(), period, column)


def add_ema(
    df: pd.DataFrame, period: int = DEFAULT_EMA_PERIOD, column: str = PRICE_COLUMN
) -> pd.DataFrame:
    """Добавляет экспоненциальную скользящую среднюю (EMA). Входной DataFrame не меняется."""
    _validate(df, period, column)
    return _apply_ema(df.copy(), period, column)


def add_rsi(
    df: pd.DataFrame, period: int = DEFAULT_RSI_PERIOD, column: str = PRICE_COLUMN
) -> pd.DataFrame:
    """Добавляет индекс относительной силы (RSI). Входной DataFrame не меняется."""
    _validate(df, period, column)
    return _apply_rsi(df.copy(), period, column)


def add_bollinger_bands(
    df: pd.DataFrame,
    period: int = DEFAULT_BB_PERIOD,
    std: float = DEFAULT_BB_STD,
    column: str = PRICE_COLUMN,
) -> pd.DataFrame:
    """Добавляет полосы Боллинджера. Входной DataFrame не меняется."""
    _validate(df, period, column)
    if std <= 0:
        raise ValueError(f"std должен быть положительным, получено {std}")
    return _apply_bollinger(df.copy(), period, std, column)


def compute_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Вычисляет полный набор индикаторов.

    Копия снимается один раз, дальше работают внутренние хелперы —
    так избегаем четырёх лишних копий DataFrame.

    Raises:
        ValueError: Если набор пуст.
        KeyError: Если отсутствует колонка close.
    """
    _validate(df, DEFAULT_SMA_PERIOD, PRICE_COLUMN)
    result = df.copy()
    result = _apply_sma(result, DEFAULT_SMA_PERIOD, PRICE_COLUMN)
    result = _apply_ema(result, DEFAULT_EMA_PERIOD, PRICE_COLUMN)
    result = _apply_rsi(result, DEFAULT_RSI_PERIOD, PRICE_COLUMN)
    result = _apply_bollinger(result, DEFAULT_BB_PERIOD, DEFAULT_BB_STD, PRICE_COLUMN)
    return result
