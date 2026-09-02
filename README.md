# Unified Task Manager

[![CI/CD Pipeline](https://github.com/actions/workflow_dispatch/badge.svg)](https://github.com/actions/workflow_dispatch)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Unified Task Manager** — это платформа для оркестрации и автоматизации рабочих процессов с использованием нескольких AI-моделей. Она предоставляет универсальный API, совместимый с OpenAI, что позволяет интегрировать ее с широким спектром инструментов, таких как LangChain, AutoGen и Cursor.

## ✨ Ключевые возможности

*   **OpenAI-Compatible API**: Используйте платформу как замену OpenAI API. Эндпоинты `/v1/models` и `/v1/chat/completions` полностью совместимы.
*   **Гибкая маршрутизация моделей**: Динамически направляйте запросы к разным AI-моделям (локальным или облачным) через конфигурацию "ролей".
*   **Оркестрация (Pipelines)**: Создавайте цепочки из нескольких AI-моделей для последовательной обработки одной задачи (например, `генератор -> аудитор -> рефактор`).
*   **REST API и CLI**: Управляйте задачами, пользователями и конфигурациями через полнофункциональный REST API или удобный CLI.
*   **Продакшн-готовность**: Проект включает структурированное логирование, мониторинг, аутентификацию (JWT), RBAC и поддержку Docker.
*   **Асинхронность**: Построен на FastAPI и SQLAlchemy 2.0, что обеспечивает высокую производительность.

## 🛠️ Технологический стек

| Категория       | Технология                                                               |
| --------------- | ------------------------------------------------------------------------ |
| **Бэкенд**      | Python 3.12+, FastAPI, Uvicorn                                           |
| **База данных** | SQLAlchemy 2.0, Alembic, PostgreSQL (рекомендуется), SQLite (для разработки) |
| **API**         | Pydantic, REST, OpenAI-совместимый интерфейс                             |
| **Безопасность**| JWT, Passlib, CORS                                                       |
| **Развертывание**| Docker, Docker Compose                                                   |
| **CI/CD**       | GitHub Actions, Pytest, Flake8, Black, Mypy                              |
| **Инструменты** | Makefile, pre-commit                                                     |

## 🚀 Быстрый старт (Docker)

Это рекомендуемый и самый простой способ запустить проект. Docker Compose автоматически подхватывает переменные из файла `.env`.

### 1. Предварительные требования

*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/) v2+

### 2. Установка

> Проект уже лежит на диске — **`git clone` не нужен**. Просто перейдите в каталог проекта. Клонирование имеет смысл только при установке на **другую** машину с GitHub/GitLab.

```bash
# 1. Перейдите в каталог проекта
cd /path/to/Test-work

# 2. Создайте файл с переменными окружения (если ещё нет)
cp .env.example .env

# 3. Задайте обязательные секреты (минимум 32 символа)
python -c "import secrets; print(secrets.token_urlsafe(32))"  # повторите 3 раза
# Отредактируйте .env: ADMIN_PASSWORD, API_SECRET_KEY, MASTER_API_KEY

# 4. Запустите сервис (по умолчанию SQLite)
docker compose up -d --build

# 5. (Опционально) PostgreSQL вместо SQLite
# В .env установите DB_TYPE=postgres, затем:
docker compose --profile postgres up -d --build
```

### 3. Готово!

| Режим | Адрес (на этой машине) | Адрес из локальной сети | Примечание |
| ----- | ---------------------- | ---------------------- | ---------- |
| Docker | [http://localhost:8002](http://localhost:8002) | [http://192.168.2.1:8002](http://192.168.2.1:8002) | порт `8002` → `8000` в контейнере |
| Локально | [http://127.0.0.1:8000](http://127.0.0.1:8000) | [http://192.168.2.1:8000](http://192.168.2.1:8000) | нужен `--host 0.0.0.0` (см. ниже) |

*   **Web UI (дашборд)**: `/` или `/login`
*   **Swagger**: `/docs`
*   **PostgreSQL** (если включён профиль `postgres`): `localhost:5433` (только с хоста, не из LAN)

### Доступ из локальной сети (192.168.2.0/24)

Сервис развёрнут в домашней сети с шлюзом/хостом **`192.168.2.1`**. С других устройств (телефон, второй ПК, Cursor на другой машине) используйте этот IP вместо `localhost`.

**Docker** — после `docker compose up -d` сервис уже слушает все интерфейсы, достаточно открыть:

`http://192.168.2.1:8002`

**Локальный запуск** — по умолчанию `make dev` привязан к `127.0.0.1` и недоступен из LAN. Запускайте так:

```bash
task-manager start-web --host 0.0.0.0 --port 8000
# или
uvicorn unified_manager.api.app:app --reload --host 0.0.0.0 --port 8000
```

**CORS** — добавьте LAN-адреса в `.env`:

```bash
ALLOWED_ORIGINS=http://localhost:8000,http://localhost:8002,http://192.168.2.1:8000,http://192.168.2.1:8002
```

**LLM-бэкенды** в той же сети — укажите IP хоста с моделью, например:

```bash
ORCHESTRATOR_BASE_URL=http://192.168.2.1:8081
CODER_BASE_URL=http://192.168.2.1:8081
```
