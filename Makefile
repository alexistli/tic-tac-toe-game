NAME := tic-tac-toe-game
POETRY := $(shell command -v poetry 2> /dev/null)
NOX := $(shell command -v nox 2> /dev/null)
DOCKER-COMPOSE := $(shell command -v docker-compose 2> /dev/null)


.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo ""
	@echo "  install		install packages and prepare environment"
	@echo "  clean			remove all temporary files"
	@echo "  start			build docker images and start web app containers"
	@echo "  stop			stop running containers"

	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

.PHONY: install
install: pyproject.toml poetry.lock
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) install

.PHONY: clean
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf .coverage .mypy_cache .nox .pytest_cache dist
	rm -rf src/app/static/dist src/app/static/.webassets-cache

.PHONY: freeze
freeze:
	$(POETRY) export -f requirements.txt --output requirements.txt --without-hashes

.PHONY: start
start: freeze
	$(DOCKER-COMPOSE) -f docker-compose.prod.yml up --build

.PHONY: stop
stop:
	$(DOCKER-COMPOSE) -f docker-compose.prod.yml down -v
