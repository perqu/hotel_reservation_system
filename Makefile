PYTHON = python
PIP = pip
PROJECT_NAME = hotel_reservation_system

.PHONY:  run

pc:
	poetry run pre-commit run --all-files

run:
	docker-compose up --build
