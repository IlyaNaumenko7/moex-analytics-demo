"""Проверка ключевого архитектурного решения: демо не зависит от внешних API."""
from __future__ import annotations

import runpy
import socket
from pathlib import Path

import pytest


class NetworkBlockedError(RuntimeError):
    """Любая попытка выйти в сеть внутри теста — ошибка."""


@pytest.fixture
def no_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def deny(*args: object, **kwargs: object) -> None:
        raise NetworkBlockedError("Сеть запрещена: демо должно работать офлайн")

    monkeypatch.setattr(socket, "socket", deny)
    monkeypatch.setattr(socket, "create_connection", deny)
    monkeypatch.setattr(socket, "getaddrinfo", deny)


def test_demo_works_without_external_api(
    project_root: Path,
    no_network: None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(project_root)
    runpy.run_path(str(project_root / "main.py"), run_name="__main__")