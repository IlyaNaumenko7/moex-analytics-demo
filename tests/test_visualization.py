"""Unit-тесты визуализации: путь, санитизация имени и валидация входа."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.indicators import compute_all_indicators
from src.mock_data import generate_mock_ohlcv
from src.visualization import plot_analysis


def test_creates_png_file(tmp_path: Path) -> None:
    df = compute_all_indicators(generate_mock_ohlcv(days=60))
    path = plot_analysis(df, "SBER_DEMO", output_dir=tmp_path)

    assert path.exists()
    assert path.suffix == ".png"


def test_unsafe_ticker_cannot_escape_output_dir(tmp_path: Path) -> None:
    df = generate_mock_ohlcv(days=30)
    path = plot_analysis(df, "../evil/ticker", output_dir=tmp_path)

    assert path.parent == tmp_path
    assert "/" not in path.name
    assert "\\" not in path.name


def test_missing_required_column_raises(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="отсутствуют колонки"):
        plot_analysis(pd.DataFrame({"open": [1.0]}), "X", output_dir=tmp_path)
