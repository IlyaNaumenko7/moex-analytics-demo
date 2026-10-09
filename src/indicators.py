"""Модуль для расчёта технических индикаторов."""

import pandas as pd
import ta


def add_sma(df: pd.DataFrame, period: int = 20, column: str = "close") -> pd.DataFrame:
    """Добавляет простую скользящую среднюю (SMA)."""
    df[f"sma_{period}"] = ta.trend.sma_indicator(df[column], window=period)
    return df


def add_ema(df: pd.DataFrame, period: int = 20, column: str = "close") -> pd.DataFrame:
    """Добавляет экспоненциальную скользящую среднюю (EMA)."""
    df[f"ema_{period}"] = ta.trend.ema_indicator(df[column], window=period)
    return df


def add_rsi(df: pd.DataFrame, period: int = 14, column: str = "close") -> pd.DataFrame:
    """Добавляет индекс относительной силы (RSI)."""
    df[f"rsi_{period}"] = ta.momentum.rsi(df[column], window=period)
    return df


def add_bollinger_bands(
    df: pd.DataFrame, period: int = 20, std: float = 2.0, column: str = "close"
) -> pd.DataFrame:
    """Добавляет полосы Боллинджера."""
    indicator = ta.volatility.BollingerBands(
        close=df[column], window=period, window_dev=std
    )
    df["bb_upper"] = indicator.bollinger_hband()
    df["bb_middle"] = indicator.bollinger_mavg()
    df["bb_lower"] = indicator.bollinger_lband()
    return df


def compute_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Вычисляет полный набор индикаторов для аналитики."""
    df = add_sma(df, period=20)
    df = add_ema(df, period=20)
    df = add_rsi(df, period=14)
    df = add_bollinger_bands(df, period=20)
    return df