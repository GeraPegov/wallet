FROM python:3.11-slim

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser
WORKDIR /app
RUN chown appuser:appuser /app 
USER appuser

COPY --chown=appuser:appuser requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 
COPY --chown=appuser:appuser . .

RUN find . -type d -name "__pycache__" -exec rm -rf {} +

CMD ["sh", "-c", "while ! pg_isready -h postgres -p 5432 -U ${POSTGRES_USER}; do sleep 1; done && \
    python -m alembic upgrade head && \
    exec python -m uvicorn main:app --host 0.0.0.0 --port 8000"]