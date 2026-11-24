FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MPLBACKEND=Agg

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

RUN mkdir -p output \
    && useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

CMD ["python", "main.py"]