"""Генератор реалистичных синтетических OHLCV-данных."""

from __future__ import annotations

import numpy as np
import pandas as pd


def generate_mock_ohlcv(days: int = 500, seed: int | None = 42) -> pd.DataFrame:
    """Генерирует синтетические OHLCV-данные, имитирующие реальную биржу.

    Args:
        days: Количество торговых дней (положительное).
        seed: Зерно ГСЧ для воспроизводимости. None — недетерминированный режим.

    Returns:
        DataFrame с колонками date, open, high, low, close, volume.

    Raises:
        ValueError: Если days <= 0.
    """
    if days <= 0:
        raise ValueError("days должен быть положительным числом")

    # Локальный ГСЧ: не трогаем глобальное состояние np.random
    rng = np.random.default_rng(seed)

    # Только торговые дни — выходные биржа не работает
    dates = pd.bdate_range(start="2023-01-02", periods=days)

    base_price = 250.0
    returns = rng.normal(0.0005, 0.015, days)
    close = base_price * np.cumprod(1 + returns)
    open_ = close * (1 + rng.uniform(-0.005, 0.005, days))

    # Инвариант OHLC: high/low накрывают тело свечи (и open, и close)
    body_high = np.maximum(open_, close)
    body_low = np.minimum(open_, close)
    high = body_high * (1 + np.abs(rng.normal(0.0, 0.01, days)))
    low = body_low * (1 - np.abs(rng.normal(0.0, 0.01, days)))

    return pd.DataFrame(
        {
            "date": dates,
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": rng.integers(5_000_000, 50_000_000, days),
        }
    )
