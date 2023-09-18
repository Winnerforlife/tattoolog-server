DOCKER_COMPOSE = docker-compose
DOCKER_EXEC = $(DOCKER_COMPOSE) exec web
PYTHON_MANAGE = $(DOCKER_EXEC) python manage.py

# Запустить контейнеры Docker
up:
	$(DOCKER_COMPOSE) up -d

# Завершить контейнеры Docker
down:
	$(DOCKER_COMPOSE) down

# Собрать контейнеры Docker
build:
	$(DOCKER_COMPOSE) up -d --build

# Перебилдить контейнер backend
build_backend:
	$(DOCKER_COMPOSE) up --build web

# Создать миграции
mm:
	$(PYTHON_MANAGE) makemigrations

# Применить миграции
m:
	$(PYTHON_MANAGE) migrate

# Создать административного пользователя (superuser)
createsuperuser:
	$(PYTHON_MANAGE) createsuperuser

# Открыть backend shell
shell:
	$(PYTHON_MANAGE) shell

# Запустить Django-сервер
run:
	$(PYTHON_MANAGE) runserver 0.0.0.0:8000

# Принять все страны и города из модуля django-cities-light
cities:
	$(PYTHON_MANAGE) cities_light

# Добавить зависимости в requirements.txt
freeze:
	pip freeze > requirements.txt

# Помощь (список доступных команд)
help:
	@echo "Доступные команды:"
	@echo "  up                 - Запустить контейнеры Docker"
	@echo "  down               - Завершить контейнеры Docker"
	@echo "  build              - Собрать контейнеры Docker"
	@echo "  build_backend      - Перебилдить контейнер backend"
	@echo "  mm                 - Создать миграции"
	@echo "  m                  - Применить миграции"
	@echo "  createsuperuser    - Создать административного пользователя (superuser)"
	@echo "  run                - Запустить Django-сервер"
	@echo "  shell              - Открыть backend shell"
	@echo "  cities             - Принять все страны и города из модуля django-cities-light"
	@echo "  freeze             - Добавить зависимости в requirements.txt"
