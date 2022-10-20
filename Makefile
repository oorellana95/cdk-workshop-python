#.DEFAULT_GOAL := start
SHELL=/bin/bash
NOW = $(shell date +"%Y%m%d%H%M%S")
UID = $(shell id -u)
PWD = $(shell pwd)
PYTHON=$(shell which python3)

.PHONY: help
help: ## prints all targets available and their description
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: upgrade-pip
upgrade-pip: ## upgrade pip
	python -m pip install --upgrade pip

.PHONY: dev-dependencies
dev-dependencies:  pyproject.toml ## install development dependencies
	(. venv/bin/activate; \
	pip install -U pip poetry; \
	poetry install)

.PHONY: app-dependencies
app-dependencies: pyproject.toml ## install application dependencies
	(. venv/bin/activate; \
	pip install -U pip poetry; \
	poetry install --no-dev)

.PHONY: all-dependencies
all-dependencies: app-dependencies dev-dependencies ## install all dependencies

.PHONY: lint
lint: ## check source code for style errors
	flake8 . && black . --check

.PHONY: format
format: ## automa tic source code formatter following a strict set of standards
	isort . --sp .isort.cfg && black .

.PHONY: venv
venv:  ## creates a virtualenv if does not exist and activates it
	@if [[ "${PYTHON_VERSION}" != "${PY_VER}" ]]; then \
       echo "You need Python ${PY_VER}. Detected ${PYTHON_VERSION}"; exit 1; \
    fi
		test -d venv || ${PYTHON} -m venv venv # setup a python3 virtualenv

.PHONY: install
install: venv all-dependencies ## Create venv and install all dependencies


.PHONY: tests
tests:  ## Run unit and integration tests
	pytest --cov

.PHONY: coverage-report
coverage-report: ## coverage report of all tests
	coverage run -m unittest discover
	coverage html
	open htmlcov/index.html
