`Tattoolog (Server side)`
=========================

Описание
---------

Этот проект представляет собой Django-приложение, которое разворачивается в контейнерах Docker. Проект включает в себя следующие сервисы:

- **web**: ``Django-сервер, который обрабатывает запросы на порту 8000.``
- **db**: ``Сервер PostgreSQL для хранения данных приложения.``
- **make help**: ``Документация к Makefile``

Установка и Запуск
-------------------

Для запуска проекта вам понадобится Docker и Docker Compose. Убедитесь, что они установлены на вашем компьютере.

1. Склонируйте репозиторий проекта:
::
    git clone https://github.com/Winnerforlife/tattoolog-server.git

2. Перейдите в каталог проекта:
::
    cd Tattoolog

3. Создайте файл `.env` для настройки переменных окружения. Вот пример файла `.env`:
::
    SECRET_KEY=''
    DEBUG=True
    ALLOWED_HOSTS="127.0.0.1 localhost 0.0.0.0"

    PG_DATABASE=postgres
    PG_USER=postgres
    PG_PASSWORD=postgres
    DB_HOST=db
    DB_PORT=5432
    WEB_PORT=8000

    EMAIL_HOST_PASSWORD='zollknhrvwujnlcf'
    DEFAULT_FROM_EMAIL='example@gmail.com'
    EMAIL_HOST_USER='example@gmail.com'

4. Создайте и запустите контейнеры Docker:
::
    make build

5. Примените миграции к базе данных:
::
    make mm && make m

6. Загрузить города и страны в БД:
::
    make cities

7. Запустите сервер:
::
    make run
