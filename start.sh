#!/bin/sh
set -e

# Применяем миграции
alembic upgrade head

until pg_isready -h db -p 5432 -U "$DB_USER"; do
  sleep 2
done

# Запускаем приложение
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
