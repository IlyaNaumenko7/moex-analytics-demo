"""Точка входа для демо-анализа исторических биржевых данных."""

import logging
from src.indicators import compute_all_indicators
from src.visualization import plot_analysis
from src.mock_data import generate_mock_ohlcv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

def main() -> None:
    ticker = "SBER_DEMO"

    logger.info(f"Генерация тестовых OHLCV-данных (имитация MOEX) для {ticker}...")
    df = generate_mock_ohlcv(days=500)
    logger.info(f"Сгенерировано {len(df)} свечей")

    logger.info("Расчёт технических индикаторов (SMA, EMA, RSI, Bollinger)...")
    df = compute_all_indicators(df)

    logger.info("Построение графика...")
    path = plot_analysis(df, ticker)
    logger.info(f"✅ Готово! График успешно сохранён: {path}")

if __name__ == "__main__":
    main()