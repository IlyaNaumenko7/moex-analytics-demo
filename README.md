# MOEX Analytics Demo

![CI](https://github.com/IlyaNaumenko7/moex-analytics-demo/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Code style](https://img.shields.io/badge/code%20style-black-000000)
![Checked with mypy](https://img.shields.io/badge/types-mypy-blue)

Демонстрационный проект аналитической системы для работы с историческими биржевыми данными.

## 🎯 Цель проекта

Показать чистую модульную архитектуру для загрузки финансовых данных, расчёта технических
индикаторов и визуализации результатов — с типизацией, линтерами и автоматическими тестами.

> **Архитектурное решение.** В демо-версии источником данных служит генератор реалистичных
> синтетических OHLCV-данных (`mock_data`). Это гарантирует стабильную работу без зависимости
> от лимитов, CORS и изменений внешних API (MOEX ISS, Yahoo Finance). Подключение реального
> API или локального CSV — реализация одного класса-адаптера, бизнес-логика не меняется.
> Работа офлайн проверяется автоматическим тестом `tests/test_offline.py`.

## 🛠 Стек

- **Python 3.11+**
- **pandas, numpy** — обработка и анализ данных
- **ta** — расчёт технических индикаторов
- **matplotlib** — визуализация (headless-режим `Agg`)
- **pytest** — unit / smoke / архитектурные тесты
- **mypy, flake8, black** — типизация и качество кода
- **Docker** — воспроизводимое окружение
- **GitHub Actions** — CI: формат, линт, типы, тесты на каждый push

## 📂 Структура

```
moex-analytics-demo/
├── src/
│   ├── __init__.py
│   ├── data_loader.py     # Граница ввода-вывода: абстракция источника данных
│   ├── indicators.py      # Расчёт технических индикаторов (без сети)
│   ├── visualization.py   # Построение графиков (без сети)
│   └── mock_data.py       # Генератор реалистичных OHLCV-данных
├── tests/
│   ├── conftest.py
│   ├── test_smoke.py         # Запуск и наличие результата
│   ├── test_offline.py       # Работа при полностью отключённой сети
│   └── test_architecture.py  # Слои не зависят от сетевых библиотек
├── output/                # Результаты (в .gitignore)
├── main.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
└── README.md
```

## 🚀 Запуск в Docker (рекомендуется)

```bash
docker build -t moex-analytics-demo .
docker run --rm -v "$(pwd)/output:/app/output" moex-analytics-demo
```

График появится в `./output/`. Windows PowerShell: `${PWD}/output` вместо `$(pwd)/output`.

## 🐍 Локальный запуск

```bash
git clone https://github.com/IlyaNaumenko7/moex-analytics-demo.git
cd moex-analytics-demo

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
python main.py
```

## ✅ Проверки качества

```bash
pip install -r requirements-dev.txt

black .          # форматирование
flake8 .         # линт
mypy src         # проверка типов
pytest -q        # тесты
```

Покрытие:

```bash
pytest --cov=src --cov-report=term-missing
```

## 🔌 Подключение реального источника данных

1. Реализовать класс-адаптер с тем же интерфейсом, что у загрузчика моков.
2. Подставить его в `main.py` вместо `mock_data`.
3. Модули `indicators` и `visualization` остаются без изменений — на этом построены
   архитектурные тесты.

## 👨‍💻 Об авторе

**Илья Науменко** — Fullstack-разработчик (Python / Java).
GitHub: [@IlyaNaumenko7](https://github.com/IlyaNaumenko7)