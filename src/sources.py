"""Адаптеры источников данных, приведённые к единому контракту OHLCVDataSource."""

from __future__ import annotations

import pandas as pd

from src.data_loader import MOEXDataLoader
from src.mock_data import generate_mock_ohlcv


class MockSource:
    """Синтетические данные: стабильное демо без внешних зависимостей."""

    def __init__(self, days: int = 500, seed: int | None = 42) -> None:
        self._days = days
        self._seed = seed

    def load(self) -> pd.DataFrame:
        """Возвращает синтетические OHLCV-данные."""
        return generate_mock_ohlcv(days=self._days, seed=self._seed)


class YahooSource:
    """Реальные исторические данные через Yahoo Finance."""

    def __init__(self, ticker: str, start_date: str, end_date: str, interval: str = "1d") -> None:
        self._loader = MOEXDataLoader(ticker)
        self._start_date = start_date
        self._end_date = end_date
        self._interval = interval

    def load(self) -> pd.DataFrame:
        """Возвращает реальные OHLCV-данные, нормализованные загрузчиком."""
        return self._loader.get_history(
            start_date=self._start_date,
            end_date=self._end_date,
            interval=self._interval,
        )
