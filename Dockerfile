FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MPLBACKEND=Agg

WORKDIR /app

# Сначала копируем зависимости и устанавливаем их (это кешируется)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Теперь копируем весь проект (main.py, src/ и т.д.), исключая то, что в .dockerignore
COPY . .

RUN mkdir -p output \
    && useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

CMD ["python", "main.py"]