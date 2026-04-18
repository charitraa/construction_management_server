.PHONY: help build up down restart logs shell db migrate createsuperuser test lint

help:
	@echo "Docker commands for Construction Management API"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build           - Build Docker images"
	@echo "  up              - Start all services"
	@echo "  down            - Stop all services"
	@echo "  restart         - Restart all services"
	@echo "  logs            - Show logs from all services"
	@echo "  logs-app        - Show logs from app service"
	@echo "  logs-db         - Show logs from database service"
	@echo "  shell           - Open Django shell in app container"
	@echo "  bash            - Open bash shell in app container"
	@echo "  db              - Open PostgreSQL shell"
	@echo "  migrate         - Run Django migrations"
	@echo "  makemigrations  - Create Django migrations"
	@echo "  createsuperuser - Create Django superuser"
	@echo "  collectstatic   - Collect static files"
	@echo "  test            - Run Django tests"
	@echo "  clean           - Remove Docker containers, volumes, and images"
	@echo "  rebuild         - Rebuild and restart services"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

logs-app:
	docker-compose logs -f app

logs-db:
	docker-compose logs -f db

shell:
	docker-compose exec app python manage.py shell

bash:
	docker-compose exec app bash

db:
	docker-compose exec db psql -U postgres -d construction_management

migrate:
	docker-compose exec app python manage.py migrate

makemigrations:
	docker-compose exec app python manage.py makemigrations

createsuperuser:
	docker-compose exec app python manage.py createsuperuser

collectstatic:
	docker-compose exec app python manage.py collectstatic --noinput

test:
	docker-compose exec app python manage.py test

clean:
	docker-compose down -v --rmi all

rebuild: down build up
