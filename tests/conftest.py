"""Общие фикстуры: корень проекта на sys.path и headless-backend для matplotlib."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("MPLBACKEND", "Agg")


@pytest.fixture(scope="session")
def project_root() -> Path:
    return ROOT
