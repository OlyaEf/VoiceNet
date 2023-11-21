# VoiceNet CDR Management API

## Описание
VoiceNet CDR Management API - это проект на Django REST Framework, предназначенный для управления данными о вызовах (CDR - Call Detail Records). Позволяет пользователям загружать, просматривать, фильтровать и удалять записи CDR через REST API.

## Функционал
- **API для управления CDR**: CRUD операции для записей CDR.
- **Фильтрация**: Получение CDR с фильтрацией по дате, номеру абонента и статусу вызова.
- **Обработка CSV**: Загрузка данных CDR из CSV-файлов.
- **Аутентификация и безопасность**: Защита API с помощью JWT.
- **Тестирование**: Unit и integration тесты для проверки API.

## Технологии
- Django 4.2.7
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Swagger
- Poetry

## Установка и запуск

1. Клонирование репозитория:
   ```bash
   git clone <repository_link>
   ```
   
2. Установка зависимостей через Poetry:
    ```bash
   poetry install
   ```

3. Активация виртуальной среды через Poetry:
    ```bash
    poetry shell
   ```

4. Настройка файла .env на основе .env.example.
- Применение миграций:
    ```bash
    python manage.py migrate
   ```
- Запуск сервера:
    ```bash
    python manage.py runserver
  ```

5. Использование API
Используйте Postman или любой HTTP-клиент для взаимодействия с API. Аутентификация реализована через JWT.

Примеры запросов
POST /api/token/: Получение токена.
GET /cdr/: Список всех CDR.
POST /cdr/: Создание новой записи CDR.
GET /cdr/{id}/: Детальная информация о CDR.
DELETE /cdr/{id}/: Удаление записи CDR.
Подробности в Swagger: /swagger/

6. Тестирование
- Запуск тестов:

    ```bash
    python manage.py test
   ```

- Просмотр покрытия тестами:

    ```bash
    coverage run --source='.' manage.py test
    coverage report
    ```
  