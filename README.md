# WB List Parser

Проект **WB List Parser** предназначен для автоматизированного сбора и сохранения данных о товарах с сайта Wildberries. Используя **Selenium**, собирается информация о названии, категории, параметрах и фотографиях товара, а при помощи **Celery** и **Redis** задачи по парсингу выполняются в фоне, чтобы не блокировать основной поток.

## Содержание

* [Технологии](#технологии)
* [Установка](#установка)
* [Структура проекта](#структура-проекта)
* [Модели данных](#модели-данных)
* [API-эндпоинты](#api-эндпоинты)
* [Примеры запросов](#примеры-запросов)

## Технологии

* Python 3.11
* Django 5.2
* Django REST Framework
* django-filter
* Celery (Redis в качестве брокера)
* Redis (очереди задач)
* Selenium (ChromeDriver)
* SQLite (по умолчанию, для разработки)

## Установка

### Клонирование репозитория

```bash
git clone <URL вашего репозитория>
cd wb-list-parser
```

### Виртуальное окружение

```bash
python -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

### Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Настройка Redis

* Homebrew (macOS):

```bash
brew install redis
brew services start redis
redis-cli ping  # → PONG
```

### Настройка Celery

В файле `settings.py`:

```python
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/1"
```

Запустить воркер:

```bash
celery -A wb_list_parser worker -l info
```

### Миграции и суперпользователь

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Сервер разработки

```bash
python manage.py runserver
```

## Структура проекта

```
wb_list_parser/
├─ manage.py
├─ wb_list_parser/
│   ├─ __init__.py
│   ├─ celery.py
│   ├─ settings.py
│   ├─ urls.py
│   ├─ wsgi.py
└─ parser/
    ├─ __init__.py
    ├─ admin.py
    ├─ apps.py
    ├─ filters.py
    ├─ models.py
    ├─ parser_module.py
    ├─ serializers.py
    ├─ tasks.py
    ├─ tests.py
    ├─ urls.py
    ├─ views.py
    └─ migrations/
```

## Модели данных

* **ProductCategory** (id, name)
* **Product** (id, name, price, category, articul, url)
* **ProductParams** (id, product, name, value)
* **ProductPhoto** (id, product, photo\_url)
* **ParserHistory** (id, articul, is\_completed, product)

## API-эндпоинты

Базовый URL:

```
http://<host>:<port>/api/v1/parser/
```

* `GET /products/` – список товаров
* `GET /products/<int:pk>/` – детальная информация о товаре
* `GET /categories/` – список категорий
* `GET /parser-history/` – история парсинга
* `POST /parse-products/?articules=1234,4321` – запуск парсера

## Примеры запросов

* Список товаров:

```bash
curl http://127.0.0.1:8000/api/v1/parser/products/
```

* Фильтр по категории:

```bash
curl "http://127.0.0.1:8000/api/v1/parser/products/?category=3"
```

* Поиск:

```bash
curl "http://127.0.0.1:8000/api/v1/parser/products/?search=MacBook"
```

* Детальная информация:

```bash
curl http://127.0.0.1:8000/api/v1/parser/products/7/
```

* Добавить артикулы в очередь парсера:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/parser/parse-products/?articules=258235213,7250481"
```

## Лицензия

Проект открыт для внутренних или учебных целей. Настройте собственный LICENSE-файл при необходимости.
