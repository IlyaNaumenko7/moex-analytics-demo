"""Адаптеры источников данных, приведёные к единому контракту OHLCVDataSource.

Этот модуль реализует паттерн "Стратегия": бизнес-логика зависит только от
интерфейса (Protocol), а конкретная реализация выбирается в одном месте (фабрике).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.data_loader import MOEXDataLoader
from src.data_source import OHLCV_COLUMNS
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


class CsvSource:
    """Локальный CSV-файл с историческими OHLCV-данными."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    def load(self) -> pd.DataFrame:
        """Читает CSV и приводит его к общему контракту OHLCVDataSource.

        Raises:
            FileNotFoundError: Если файл по указанному пути не существует.
            ValueError: Если в файле отсутствуют обязательные колонки.
        """
        if not self._path.exists():
            raise FileNotFoundError(f"CSV-файл не найден: {self._path}")

        df = pd.read_csv(self._path)

        # Проверяем, что файл соответствует нашему контракту
        missing_columns = [col for col in OHLCV_COLUMNS if col not in df.columns]
        if missing_columns:
            raise ValueError(
                f"В CSV отсутствуют обязательные колонки: {missing_columns}. "
                f"Ожидались: {OHLCV_COLUMNS}"
            )

        # Нормализуем даты и сортируем (чтобы поведение совпадало с YahooSource)
        df["date"] = pd.to_datetime(df["date"])

        return df[OHLCV_COLUMNS].sort_values("date").reset_index(drop=True)
