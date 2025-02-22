# ad-dicted
### ad-dicted — это рекламный движок, написанный на Python
![Python](https://img.shields.io/badge/python-python?style=for-the-badge&logo=python&logoColor=yellow&color=blue)
![Fastapi](https://img.shields.io/badge/fastapi-fastapi?style=for-the-badge&logo=fastapi&logoColor=white&color=%23009688)
![Pydantic](https://img.shields.io/badge/pydantic-pydantic?style=for-the-badge&logo=pydantic&logoColor=white&color=%23E92063)
![Sqlalchemy](https://img.shields.io/badge/sqlalchemy-sqlalchemy?style=for-the-badge&logo=sqlalchemy&logoColor=white&color=%23D71F00)
![Dishka](https://img.shields.io/badge/dishka-dishka?style=for-the-badge&logo=textpattern&logoColor=black&color=%23FFDA44)
![Ruff](https://img.shields.io/badge/ruff-ruff?style=for-the-badge&logo=ruff&logoColor=purple&color=%23D7FF64)
![Postgresql](https://img.shields.io/badge/postgresql-postgresql?style=for-the-badge&logo=postgresql&logoColor=white&color=%234169E1)
![Docker](https://img.shields.io/badge/docker-docker?style=for-the-badge&logo=docker&logoColor=white&color=%232496ED)
![S3](https://img.shields.io/badge/s3-s3?style=for-the-badge&logo=amazons3&logoColor=white&color=%23569A31)
![Yandex Cloud](https://img.shields.io/badge/yandex_cloud-yandex_cloud?style=for-the-badge&logo=yandexcloud&logoColor=white&color=%235282FF)

### Nota Bene!
Данный перевод выполнен автоматически. В случае возникновения недопониманий, пожалуйста, обратитесь к [оригиналу](README.md).

## Навигация
* [Краткое описание](#описание)
  * [Интерфейс](#интерфейс)
  * [Алгоритм](#алгоритм)
* [Быстрый старт](#быстрый-старт)
  * [Конфигурация](#конфигурация)
  * [Запуск сервиса](#запуск-сервиса)
  * [Доступ к OpenAPI](#доступ-к-openapi)
* [Технический обзор](#технический-обзор)
  * [Архитектура](#архитектура)
    * [Слои](#слои)
    * [Зависимости сервиса](#зависимости-сервиса)
    * [Хранилища данных](#хранилища-данных)
    * [Модерация и генерация текста](#модерация-и-генерация-текста)
  * [Разработка](#разработка)
    * [Управление проектом](#управление-проектом)
    * [Линтинг](#линтинг)
    * [Тестирование](#тестирование)
    * [Система контроля версий](#система-контроля-версий)
  * [Схемы](#схемы)
* [Демонстрация использования](#демонстрация-использования)
  * [API](#api)
  * [Бот](#бот)

## Описание
ad-dicted — это рекламный движок, который использует специальный алгоритм для
эффективного подбора релевантных рекламных кампаний для ваших клиентов.

### Интерфейс
ad-dicted предоставляет интерфейс, который позволяет создавать рекламодателей, пользователей и
рекламные кампании. Также можно привязывать «оценки» к парам рекламодатель-пользователь,
что позволяет интегрироваться с любым сервисом оценки релевантности.
В данном случае ad-dicted принимает «ML Scores» — внешний алгоритм машинного обучения
оценивает релевантность рекламы для пользователей, и эти оценки затем используются
в алгоритме ad-dicted.

### Алгоритм
Алгоритм ad-dicted следует двум приоритетам:

1. Прибыль
2. Релевантность (качество выдачи)

Это означает, что при выборе рекламной кампании алгоритм сначала ориентируется
на прибыль, а затем на релевантность. Формула:
* (Нормализованный CPV + Нормализованный CPC) * 2 + Нормализованный Score  
*CPV — стоимость за просмотр*  
*CPC — стоимость за клик*

Алгоритм также отдает приоритет непросмотренным кампаниям перед просмотренными.

Кроме того, ad-dicted позволяет задавать таргетинг для каждой кампании. Если таргетинг
установлен, алгоритм отфильтрует всех несовместимых пользователей.

## Быстрый старт
ad-dicted предоставляет единую точку входа — сервер на [FastAPI](https://github.com/fastapi).
Этот сервер поднимет HTTP-сервер и попытается подключиться к PostgreSQL, Yandex Cloud S3 и Yandex GPT.

### Конфигурация
Перед запуском сервиса необходимо настроить файл «.env».
Скопируйте содержимое «.env.template» в файл «.env» и заполните переменные:

...

### Запуск сервиса
Доступны два варианта запуска:

1. **Запуск вручную**
    ```shell
    uv sync  # Установка зависимостей
    source .venv/bin/activate  # Активация виртуального окружения
    fastapi run app/adapters/fastapi/main.py  # Запуск сервера
    ```
2. **Запуск через docker-compose**
    ```shell
    docker compose up --build
    ```
    Либо конкретный сервис:
    ```shell
    docker compose up [postgres,grafana,backend,bot]
    ```

### Доступ к OpenAPI
FastAPI сервер также предоставляет документацию Swagger, доступную по эндпоинту **/docs**.

## Технический обзор

### Архитектура
ad-dicted разрабатывался с учетом расширяемости и качества кода, следуя принципам **SOLID** и **Чистой архитектуры**.

#### Слои
Кодовая база ad-dicted разделена на 4 слоя:

...

#### Зависимости сервиса
...

#### Хранилища данных
...

#### Модерация и генерация текста
...

## Разработка

### Управление проектом
ad-dicted использует менеджер пакетов **uv** для управления зависимостями и виртуальными окружениями.

### Линтинг
Проект строго придерживается стандартов качества кода, используя **ruff** и **isort**.

### Тестирование
Проект содержит модульные и интеграционные тесты, не зависящие от внешних сервисов.

### Система контроля версий
Используется стандартное соглашение коммитов:

`действие(область): описание`

Пример:

`feat(infra/yandexgpt): реализован интерактор YandexGPT`

## Схемы
ad-dicted использует следующую реляционную схему SQL:
![db-schema](assets/db-schema.png)

## Демонстрация использования
### API
Вы можете протестировать API с помощью e2e тестов или вручную через Postman:
![api-usage-postman](assets/api-usage-postman.png)

### Бот
Бот является минималистичной реализацией пользовательского взаимодействия:
![addicted-bot-demo](assets/addicted-bot-demo.gif)
