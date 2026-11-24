"""Модуль визуализации результатов анализа.

Слой отвечает только за отрисовку: данные и индикаторы приходят уже готовыми.
Сетевых и вычислительных зависимостей нет — это проверяется архитектурным тестом.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes

REQUIRED_COLUMNS = ("date", "close")
FIGURE_SIZE = (14, 8)
HEIGHT_RATIOS = [3, 1]
DPI = 150

COLOR_CLOSE = "#2c3e50"
COLOR_SMA = "#e74c3c"
COLOR_EMA = "#3498db"
COLOR_BANDS = "#95a5a6"
COLOR_RSI = "#8e44ad"


def _safe_filename_part(value: str) -> str:
    """Оставляет в имени файла только безопасные символы."""
    cleaned = "".join(char if char.isalnum() or char in "-_" else "_" for char in value)
    return cleaned.strip("_") or "chart"


def _validate(df: pd.DataFrame) -> None:
    """Проверяет, что набор данных пригоден для отрисовки."""
    if df.empty:
        raise ValueError("DataFrame пуст — нечего визуализировать")

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Для построения графика отсутствуют колонки: {missing}")


def _draw_price_panel(ax: Axes, df: pd.DataFrame, ticker: str) -> None:
    """Верхняя панель: цена, скользящие средние и полосы Боллинджера."""
    ax.plot(df["date"], df["close"], label="Close", color=COLOR_CLOSE, linewidth=1.5)

    if "sma_20" in df.columns:
        ax.plot(df["date"], df["sma_20"], label="SMA 20", color=COLOR_SMA, linewidth=1)
    if "ema_20" in df.columns:
        ax.plot(df["date"], df["ema_20"], label="EMA 20", color=COLOR_EMA, linewidth=1)

    # Границы берём только если присутствуют обе — иначе fill_between упадёт
    if {"bb_upper", "bb_lower"} <= set(df.columns):
        ax.fill_between(
            df["date"],
            df["bb_lower"],
            df["bb_upper"],
            alpha=0.15,
            color=COLOR_BANDS,
            label="Bollinger Bands",
        )

    ax.set_title(f"{ticker} — Price & Indicators", fontsize=14, fontweight="bold")
    ax.set_ylabel("Price (RUB)")
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)


def _draw_rsi_panel(ax: Axes, df: pd.DataFrame) -> None:
    """Нижняя панель: RSI с зонами перекупленности и перепроданности."""
    if "rsi_14" not in df.columns:
        ax.set_visible(False)
        return

    ax.plot(df["date"], df["rsi_14"], label="RSI 14", color=COLOR_RSI, linewidth=1.2)
    ax.axhline(70, color="red", linestyle="--", alpha=0.5)
    ax.axhline(30, color="green", linestyle="--", alpha=0.5)
    ax.fill_between(df["date"], 30, 70, alpha=0.05, color="gray")
    ax.set_ylabel("RSI")
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)


def plot_analysis(df: pd.DataFrame, ticker: str, output_dir: str | Path = "output") -> Path:
    """Строит сводный график и сохраняет его в PNG.

    Args:
        df: DataFrame с колонками date и close, опционально — с индикаторами
            (sma_20, ema_20, bb_upper, bb_lower, rsi_14).
        ticker: Подпись инструмента. Небезопасные символы в имени файла
            заменяются на подчёркивание.
        output_dir: Каталог для сохранения PNG, создаётся при отсутствии.

    Returns:
        Путь к сохранённому файлу.

    Raises:
        ValueError: Если набор пуст или отсутствуют обязательные колонки.
    """
    _validate(df)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    file_path = output_path / f"{_safe_filename_part(ticker)}_analysis.png"

    fig, (ax1, ax2) = plt.subplots(
        2,
        1,
        figsize=FIGURE_SIZE,
        gridspec_kw={"height_ratios": HEIGHT_RATIOS},
        sharex=True,
    )

    # Фигура закрывается даже при ошибке отрисовки — иначе течёт память
    try:
        _draw_price_panel(ax1, df, ticker)
        _draw_rsi_panel(ax2, df)

        # Подпись оси ставим на нижнюю видимую панель
        if ax2.get_visible():
            ax2.set_xlabel("Date")
        else:
            ax1.set_xlabel("Date")
            ax1.tick_params(labelbottom=True)

        fig.tight_layout()
        fig.savefig(file_path, dpi=DPI, bbox_inches="tight")
    finally:
        plt.close(fig)

    return file_path
