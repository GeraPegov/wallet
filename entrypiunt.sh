#!/bin/sh

# Проверка доступности PostgreSQL
until pg_isready -h postgres -p 5432 -U ${POSTGRES_USER}
do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

# Применение миграций
python -m alembic upgrade head

# Запуск приложения
exec uvicorn app.main:app --host 0.0.0.0 --port 8000