"""Контракт источника данных: бизнес-логика зависит от абстракции, не от реализации."""

from __future__ import annotations

from typing import Protocol

import pandas as pd

OHLCV_COLUMNS = ["date", "open", "high", "low", "close", "volume"]


class OHLCVDataSource(Protocol):
    """Единый интерфейс источника исторических OHLCV-данных."""

    def load(self) -> pd.DataFrame:
        """Вернуть DataFrame с колонками date, open, high, low, close, volume."""
        ...
