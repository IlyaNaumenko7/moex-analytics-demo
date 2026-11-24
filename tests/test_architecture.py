"""Архитектурные проверки: слои разделены, бизнес-логика не знает о сети."""

from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest

NETWORK_MODULES = {"requests", "httpx", "aiohttp", "urllib", "urllib3", "socket"}
PURE_LAYERS = ["indicators.py", "visualization.py", "mock_data.py"]
MODULES = ["data_loader", "indicators", "visualization", "mock_data"]


def _imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    return names


@pytest.mark.parametrize("module", PURE_LAYERS)
def test_business_logic_has_no_network_dependencies(project_root: Path, module: str) -> None:
    path = project_root / "src" / module
    assert path.exists(), f"Ожидался модуль {path}"
    leaked = _imported_roots(path) & NETWORK_MODULES
    assert not leaked, f"{module} не должен зависеть от сети, найдено: {leaked}"


@pytest.mark.parametrize("name", MODULES)
def test_layers_import_independently(name: str) -> None:
    assert importlib.import_module(f"src.{name}") is not None
