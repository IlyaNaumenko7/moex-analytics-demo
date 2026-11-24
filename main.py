"""Точка входа для демо-анализа исторических биржевых данных."""

from __future__ import annotations

import logging

from src.data_source import OHLCVDataSource
from src.indicators import compute_all_indicators
from src.sources import MockSource
from src.visualization import plot_analysis

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

TICKER = "SBER_DEMO"


def build_source() -> OHLCVDataSource:
    """Фабрика источника данных.

    Единственное место, где выбирается реализация. Для перехода на реальные
    данные достаточно заменить возвращаемый адаптер — тело main() не меняется.
    """
    return MockSource(days=500)
    # return YahooSource(
    #     ticker="SBER", start_date="2024-01-01", end_date="2024-12-31"
    # )


def main() -> None:
    source = build_source()

    logger.info("Загрузка OHLCV-данных для %s...", TICKER)
    df = source.load()
    logger.info("Загружено %d свечей", len(df))

    logger.info("Расчёт технических индикаторов (SMA, EMA, RSI, Bollinger)...")
    df = compute_all_indicators(df)

    logger.info("Построение графика...")
    path = plot_analysis(df, TICKER)
    logger.info("Готово. График сохранён: %s", path)


if __name__ == "__main__":
    main()
