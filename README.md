# TaskTracker Project
Проект для управления задачами с интеграцией Telegram бота.

# Технологии
Backend: Django + Django REST Framework

Database: PostgreSQL

Message Broker: Redis

Task Queue: Celery + Celery Beat

Containerization: Docker + Docker Compose

Web Server: Nginx

Bot: Telegram Bot API

# Требования
## Для запуска в Docker:
Docker 20.10+

Docker Compose 2.0+

## Для ручного запуска:
Python 3.9+

PostgreSQL 14+

Redis 7+

# Быстрый запуск через Docker

## 1. Клонирование и настройка
    
    git clone https://github.com/Arty525/ChatLabs
    cd tasktracker

## 2. Создание .env файла

    DB_NAME=your_db_name

    DB_USER=your_db_user
    
    DB_PASSWORD=your_db_password
    
    DB_HOST=your_host
    
    DB_PORT=your_db_port
    
    TG_WEBHOOK_URL=your_tg_webhook_url
    
    TG_TOKEN=your_tg_token
    
    TG_WEBHOOK_SECRET=your_tg_webhook_secret
    
    API_BASE_URL=your_api_base_url

## 3. Запуск контейнеров

    docker-compose up -d

## 4. Проверка статуса

    docker-compose ps

## 5. Просмотр логов

    # Все логи
    docker-compose logs
    
    # Логи конкретного сервиса
    docker-compose logs web
    docker-compose logs celery
    docker-compose logs bot

## 6. Остановка

    docker-compose down

# Ручная установка и запуск

## 1. Установка зависимостей

    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # или
    venv\Scripts\activate  # Windows
    
    pip install -r requirements.txt

## 2. Настройка базы данных

    # Создание базы данных в PostgreSQL
    sudo -u postgres psql
    CREATE DATABASE tasktracker_db;
    CREATE USER postgres WITH PASSWORD 'NewArt334472';
    GRANT ALL PRIVILEGES ON DATABASE tasktracker_db TO postgres;
    \q

## 3. Настройка переменных окружения

    Создайте .env файл:
        DB_NAME=your_db_name
        
        DB_USER=your_db_user
        
        DB_PASSWORD=your_db_password
        
        DB_HOST=your_host
        
        DB_PORT=your_db_port
        
        TG_WEBHOOK_URL=your_tg_webhook_url
        
        TG_TOKEN=your_tg_token
        
        TG_WEBHOOK_SECRET=your_tg_webhook_secret
        
        API_BASE_URL=your_api_base_url

## 4. Запуск Redis

    # Ubuntu/Debian
    sudo apt update
    sudo apt install redis-server
    sudo systemctl start redis
    
    # MacOS
    brew install redis
    brew services start redis
    
    # Windows
    # Скачайте и установите Redis с официального сайта

## 5. Миграции и статические файлы

    python manage.py migrate
    python manage.py collectstatic --noinput

## 6. Запуск сервисов

    # Терминал 1: Django сервер
    python manage.py runserver
    
    # Терминал 2: Celery worker
    celery -A config worker --loglevel=info
    
    # Терминал 3: Celery beat
    celery -A config beat --loglevel=info
    
    # Терминал 4: Telegram бот
    python manage.py run_bot

# Стурктура проекта

ChatLabs/
├── docker-compose.yaml
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf
├── config/                 # Django settings
├── tasktracker/             # Приложение задач
├── users/             # Приложение пользователей
├── bot/      # Telegram бот
├── requirements.txt
├── manage.py
└── .env

# Доступные сервисы
## После запуска:

Django приложение: http://localhost:8000

Admin панель: http://localhost:8000/admin

API: http://localhost:8000/api/

Nginx: http://localhost:8080 (только в Docker)

PostgreSQL: localhost:5432

Redis: localhost:6379

# Полезные команды

## Docker команды

    # Пересборка образов
    docker-compose build --no-cache
    
    # Запуск конкретного сервиса
    docker-compose up -d web celery
    
    # Выполнение команд в контейнере
    docker-compose exec web python manage.py createsuperuser
    docker-compose exec db psql -U postgres -d tasktracker_db
    
    # Просмотр логов в реальном времени
    docker-compose logs -f web

## Django команды

    # Создание суперпользователя
    python manage.py createsuperuser
    
    # Запуск тестов
    python manage.py test
    
    # Создание миграций
    python manage.py makemigrations
    
    # Проверка здоровья
    curl http://localhost:8000/health/
