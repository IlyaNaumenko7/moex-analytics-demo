"""Smoke-тест: точка входа отрабатывает и сохраняет график."""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path


def test_main_runs_and_produces_chart(project_root: Path) -> None:
    start = time.time()

    result = subprocess.run(
        [sys.executable, "main.py"],
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=180,
    )

    assert result.returncode == 0, (
        f"main.py завершился с ошибкой:\n{result.stdout}\n{result.stderr}"
    )

    charts = [
        p
        for p in project_root.rglob("*.png")
        if p.stat().st_mtime >= start - 1
        and "venv" not in p.parts
        and ".venv" not in p.parts
    ]
    assert charts, "После запуска не найдено ни одного сохранённого графика (.png)"