"""Модуль для визуализации результатов анализа."""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def plot_analysis(df: pd.DataFrame, ticker: str, output_dir: str = "output") -> Path:
    """
    Строит сводный график: цена + индикаторы + RSI.

    Args:
        df: DataFrame с данными и индикаторами.
        ticker: Тикер для подписи графика.
        output_dir: Папка для сохранения PNG.

    Returns:
        Путь к сохранённому файлу.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    file_path = output_path / f"{ticker}_analysis.png"

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(14, 8), gridspec_kw={"height_ratios": [3, 1]}, sharex=True
    )

    # Верхний график: цена + SMA/EMA + Bollinger
    ax1.plot(df["date"], df["close"], label="Close", color="#2c3e50", linewidth=1.5)
    if "sma_20" in df.columns:
        ax1.plot(df["date"], df["sma_20"], label="SMA 20", color="#e74c3c", linewidth=1)
    if "ema_20" in df.columns:
        ax1.plot(df["date"], df["ema_20"], label="EMA 20", color="#3498db", linewidth=1)

    # Bollinger Bands
    if "bb_upper" in df.columns:
        ax1.fill_between(
            df["date"], df["bb_lower"], df["bb_upper"],
            alpha=0.15, color="#95a5a6", label="Bollinger Bands"
        )

    ax1.set_title(f"{ticker} — Price & Indicators", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Price (RUB)")
    ax1.legend(loc="upper left")
    ax1.grid(alpha=0.3)

    # Нижний график: RSI
    if "rsi_14" in df.columns:
        ax2.plot(df["date"], df["rsi_14"], label="RSI 14", color="#8e44ad", linewidth=1.2)
        ax2.axhline(70, color="red", linestyle="--", alpha=0.5)
        ax2.axhline(30, color="green", linestyle="--", alpha=0.5)
        ax2.fill_between(df["date"], 30, 70, alpha=0.05, color="gray")
        ax2.set_ylabel("RSI")
        ax2.set_xlabel("Date")
        ax2.legend(loc="upper left")
        ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(file_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return file_path