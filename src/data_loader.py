"""Загрузка исторических OHLCV-данных с внешнего источника (Yahoo Finance).

Слой отвечает только за получение и нормализацию данных: расчёты и визуализация
живут в других модулях и от источника не зависят.
"""

from __future__ import annotations

import pandas as pd
import yfinance as yf

from src.data_source import OHLCV_COLUMNS

ALLOWED_INTERVALS = ("1d", "1wk", "1mo")

_COLUMN_MAP = {
    "Date": "date",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume",
}


class MOEXDataLoader:
    """Загрузчик исторических OHLCV-данных через Yahoo Finance."""

    def __init__(self, ticker: str, auto_suffix: bool = True) -> None:
        """
        Args:
            ticker: Тикер инструмента, например 'SBER' или 'AAPL'.
            auto_suffix: Если True и в тикере нет точки, добавляется '.ME'
                (рынок MOEX): 'SBER' -> 'SBER.ME'. Для других рынков передавайте
                тикер с auto_suffix=False, чтобы он остался без изменений.

        Raises:
            ValueError: Если тикер пустой.
        """
        normalized = ticker.strip().upper()
        if not normalized:
            raise ValueError("ticker не может быть пустым")

        if auto_suffix and "." not in normalized:
            normalized = f"{normalized}.ME"

        self.ticker = normalized

    def get_history(self, start_date: str, end_date: str, interval: str = "1d") -> pd.DataFrame:
        """Загружает исторические OHLCV-данные и приводит их к единому контракту.

        Args:
            start_date: Начальная дата в формате 'YYYY-MM-DD'.
            end_date: Конечная дата в формате 'YYYY-MM-DD'.
            interval: Интервал свечей: '1d', '1wk' или '1mo'.

        Returns:
            DataFrame с колонками date, open, high, low, close, volume,
            отсортированный по дате, без часового пояса.

        Raises:
            ValueError: Некорректный интервал, пустой ответ, неполный набор
                колонок или ошибка внешнего источника.
        """
        if interval not in ALLOWED_INTERVALS:
            raise ValueError(
                f"Неподдерживаемый интервал '{interval}'. "
                f"Допустимые значения: {ALLOWED_INTERVALS}"
            )

        # Оборачиваем только сетевой вызов — свои ошибки не перехватываем
        try:
            stock = yf.Ticker(self.ticker)
            raw = stock.history(start=start_date, end=end_date, interval=interval)
        except Exception as exc:
            raise ValueError(f"Ошибка загрузки данных для {self.ticker}: {exc}") from exc

        if raw.empty:
            raise ValueError(f"Нет данных для тикера {self.ticker}")

        df = raw.reset_index().rename(columns=_COLUMN_MAP)

        missing = [column for column in OHLCV_COLUMNS if column not in df.columns]
        if missing:
            raise ValueError(f"Источник вернул неполный набор колонок, отсутствуют: {missing}")

        # Устойчиво и к tz-aware, и к tz-naive датам
        dates = pd.to_datetime(df["date"])
        df["date"] = dates.dt.tz_localize(None) if dates.dt.tz is not None else dates

        return df[OHLCV_COLUMNS].sort_values("date").reset_index(drop=True)
