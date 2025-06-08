# Сервис "Wallet"

Сервис для создания кошелька и проведения транзакций.

## Требования

- Python 3.9+
- Docker и docker-compose (для контейнеризации)
- PostgreSQL

## Запуск с помощью Docker

```bash
# Клонировать репозиторий
git clone https://github.com/GeraPegov/wallet
cd wallet

# Запустить с помощью Docker-compose
docker-compose up -d
```

Сервис будет доступен по адресу: http://localhost:8000

## Запуск без Docker

```bash
# Клонировать репозиторий
git clone https://github.com/GeraPegov/wallet
cd wallet

# Создать виртуальное окружение(Учитывайте вашу ОС)
python -m venv .venv
source .venv/bin/activate # На macOS, Linux
# ИЛИ
.\.venv\Scripts\activate # На Windows

# Установить зависимости
pip install -r requirements.txt

# Настроить миграции alembic
alembic init alembic
# Если используете свой сервер PostgreSQL - в .env пропишите путь
alembic revision --autogenerate -m "First migration"
alembic upgrade head

# Запустить сервис
uvicorn main:app --reload
```

## Конфигурация

Конфигурация может быть задана через переменные окружения в фалйе `.env`:

- `MY_DB_URL` - URL базы данных

## API

### Получение ID кошелька

```
GET /api/v1/
```

**Пример ответа:**

```json
{
  "wallet_id": "qwe123qwep",
  "status": "success"
}
```

### Пополнить счет(DEPOSIT)

```
POST /api/v1/wallets/wallet_id/operation
```

**Пример запроса:**

- `wallet_id` (str) - Номер кошелька
- `amount` (int) - Сумма пополнения

**Пример ответа:**

```json
{
  "status": "success",
  "balance": 1000
}
```

### Снять со счета(WITHDRAW)

```
POST /api/v1/wallets/wallet_id/operation
```

**Пример запроса:**

- `wallet_id` (str) - Номер кошелька
- `amount` (int) - Сумма снятия

**Пример ответа:**

```json
{
  "status": "success",
  "balance": 1000
}
```

### Баланс

```
GET /api/v1/wallets/wallet_id
```

**Пример запроса:**

- `wallet_id` (str) - Номер кошелька

**Пример ответа:**

```json
{
  "balance": 1000
}
```

## Структура базы данных

### Таблица `wallet`

- `id` = Автоинкрементное поле(может происходить поиск записи по ID)
- `wallet_id` = Генерируется в get запросе ID кошелька
- `total` = Остаток на счете

### Тестирование

Проект включает интеграционные тесты для запросов в БД и юнит тест для корректной выдачи ID кошелька

### Запуск тестов

```bash
pytest
```
