"""Генератор реалистичных тестовых OHLCV-данных."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_mock_ohlcv(days: int = 500) -> pd.DataFrame:
    """Генерирует синтетические OHLCV-данные, имитирующие реальную биржу."""
    dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(days)]

    # Генерируем цену со случайным блужданием (как на реальной бирже)
    np.random.seed(42)
    base_price = 250.0  # Базовая цена, похожая на Сбер
    returns = np.random.normal(0.0005, 0.015, days)
    prices = base_price * np.cumprod(1 + returns)

    df = pd.DataFrame({
        "date": dates,
        "open": prices * (1 + np.random.uniform(-0.005, 0.005, days)),
        "high": prices * (1 + np.abs(np.random.normal(0, 0.01, days))),
        "low": prices * (1 - np.abs(np.random.normal(0, 0.01, days))),
        "close": prices,
        "volume": np.random.randint(5_000_000, 50_000_000, days),
    })

    return df