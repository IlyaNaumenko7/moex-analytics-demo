# MOEX Analytics Demo

Демонстрационный проект аналитической системы для работы с историческими данными Московской биржи (MOEX).

## Возможности

- 📥 Загрузка исторических OHLCV-данных через MOEX API
- 📊 Расчёт технических индикаторов: SMA, EMA, RSI, Bollinger Bands
- 📈 Визуализация результатов анализа
- 🧪 Чистая модульная архитектура с типизацией

## Стек

- Python 3.11+
- pandas, numpy
- moexalgo (обёртка над MOEX ISS API)
- pandas-ta (технические индикаторы)
- matplotlib (визуализация)

## Установка

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

Результат — PNG-график в папке `output/`.

## Структура

```
src/
  data_loader.py     # загрузка данных MOEX
  indicators.py      # расчёт индикаторов
  visualization.py   # построение графиков
main.py              # точка входа
```

## Автор

Fullstack-разработчик (Python / Java). Опыт работы с финансовыми временными рядами, статистическим анализом и построением расчётных движков.