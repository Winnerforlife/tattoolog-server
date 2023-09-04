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

# Создать минрации
mm:
	$(PYTHON_MANAGE) makemigrations

# Применить миграции
m:
	$(PYTHON_MANAGE) migrate

# Создать административного пользователя (superuser)
createsuperuser:
	$(PYTHON_MANAGE) createsuperuser

# Отрыть backend shell
shell:
	$(PYTHON_MANAGE) shell

# Запустить Django-сервер
run:
	$(PYTHON_MANAGE) runserver 0.0.0.0:8000

# Помощь (список доступных команд)
help:
	@echo "Доступные команды:"
	@echo "  up                 - Запустить контейнеры Docker"
	@echo "  down               - Завершить контейнеры Docker"
	@echo "  build              - Собрать контейнеры Docker"
	@echo "  build_backend      - Перебилдить контейнеры Docker"
	@echo "  mm                 - Создать минрации"
	@echo "  m                  - Применить миграции"
	@echo "  createsuperuser    - Создать административного пользователя"
	@echo "  run                - Запустить Django-сервер"
	@echo "  shell              - Отрыть backend shell"
