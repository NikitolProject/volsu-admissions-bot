# Telegram Bot для Приёмной Комиссии ВолГУ

Этот проект представляет собой Telegram-бота для проверки статуса поступления в Волгоградский государственный университет (ВолГУ). Бот позволяет пользователям найти информацию о своём поступлении по номеру СНИЛС и администраторам обновлять базу данных поступивших.

## Требования

- Docker
- Docker Compose

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/NikitolProject/volsu-admissions-bot.git
cd volsu-admissions-bot
```

2. Создайте `.env` файл в корне проекта и заполните его следующими значениями:

```env
DATABASE_DIALECT=postgresql
DATABASE_HOSTNAME=your_db_hostname
DATABASE_NAME=your_db_name
DATABASE_USERNAME=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_PORT=5432
ADMIN_TELEGRAM_ID=your_admin_tg_id
TELEGRAM_BOT_TOKEN=your_bot_token
DEBUG_MODE=true
```

3. Запустите Docker Compose для поднятия контейнеров с ботом и базой данных:

```bash
docker-compose up --build
```

4. Примените миграции базы данных с помощью Alembic (при изменении моделей базы данных):

```bash
docker-compose run bot alembic upgrade head
```

## Использование

После успешного запуска бота и базы данных, бот будет доступен в Telegram. Администратор может обновлять базу данных, а пользователи могут искать информацию о своём поступлении.

### Команды

- `/start` - команда для начала взаимодействия с ботом. Администратор увидит кнопку для обновления базы данных, а пользователи - кнопку для поиска себя в списке поступивших.
- `♻️ Обновить БД` - кнопка для администратора, которая позволяет обновить базу данных поступивших.
- `🔍 Найти себя` - кнопка для пользователей, которая позволяет найти информацию о своём поступлении по номеру СНИЛС.

## Структура проекта

    .
    ├── alembic.ini
    ├── docker-compose.yaml
    ├── Dockerfile
    ├── main.py
    ├── requirements.txt
    └── src
        ├── application
        │   ├── schemas
        │   │   └── pydantic
        │   │       ├── __init__.py
        │   │       └── user_schema.py
        │   └── services
        │       ├── __init__.py
        │       └── user_service.py
        ├── domain
        │   ├── bot
        │   │   ├── forms
        │   │   │   ├── __init__.py
        │   │   │   └── form_factory.py
        │   │   └── handlers
        │   │       ├── __init__.py
        │   │       └── handler_factory.py
        │   ├── models
        │   │   ├── __init__.py
        │   │   ├── base_model.py
        │   │   └── user_model.py
        │   └── repositories
        │       ├── __init__.py
        │       └── repository_meta.py
        ├── infrastructure
        │   ├── configs
        │   │   ├── __init__.py
        │   │   ├── database.py
        │   │   └── enviroment.py
        │   └── database
        │   │   └── __init__.py
        │   └── repositories
        │       ├── __init__.py
        │       └── user_repository.py       
        └── interfaces
            └── bot
                ├── forms
                │   ├── __init__.py
                │   ├── export_form.py
                │   └── find_me_form.py
                └── handlers
                    ├── __init__.py
                    ├── export_handler.py
                    ├── find_me_handler.py
                    └── start_handler.py

## Примеры

### Пример файла CSV для обновления базы данных

```csv
СНИЛС;поступил;факультет
12345678901;да;МКН
23456789012;нет;ПРИ
34567890123;да;ПМИ
```
