NAME := tic-tac-toe-game
POETRY := $(shell command -v poetry 2> /dev/null)
NOX := $(shell command -v nox 2> /dev/null)

COMPOSE_FILE := docker-compose.$(ENV).yml

.DEFAULT_GOAL := help


.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo ""
	@echo "  install		install packages and prepare environment"
	@echo "  clean			remove all temporary files"
	@echo "  freeze			freeze poetry dependencies into a requirements.txt file"
	@echo "  start			start web app containers, pull or build if necessary"
	@echo "  stop			stop running containers"
	@echo "  re-start		build docker images and start web app containers"
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."


.PHONY: check-env
check-env:
ifndef ENV
	@$(error The ENV variable is missing)
endif
ifeq ($(filter $(ENV),dev prod),)
	@$(error The ENV variable is invalid: "$(ENV)")
endif


.PHONY: install
install: pyproject.toml poetry.lock
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	@$(POETRY) install
	@npm install --global postcss-cli@^8.3.1
	@cd src && npm install


.PHONY: clean
clean:
	@find . -type d -name "__pycache__" | xargs rm -rf {};
	@rm -rf .cache .coverage .mypy_cache .nox .pytest_cache dist
	@rm -rf src/app/static/dist src/app/static/.webassets-cache


.PHONY: freeze
freeze:
	@$(POETRY) export -f requirements.txt --output requirements.txt --without-hashes


.PHONY: start
start: check-env
	@$(info Make: Using "$(ENV)" environment)
	@$(info Make: Using "$(COMPOSE_FILE)" Compose file)
	@docker-compose -f $(COMPOSE_FILE) up --build


.PHONY: stop
stop:
	@docker rm -f $$(docker ps -aq -f name=^ttt-)


.PHONY: re-start
re-start: stop start
