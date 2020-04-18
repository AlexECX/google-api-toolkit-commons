.DEFAULT_GOAL := all

isort = isort -rc google_api_toolkit tests
black = black -l 88 google_api_toolkit tests

.PHONY: format
format:
	$(isort)
	$(black)

.PHONY: lint
lint:
	flake8 google_api_toolkit/ tests/
	$(isort) --check-only
	$(black) --check

.PHONY: mypy
mypy:
	mypy google_api_toolkit

.PHONY: test
test:
	pytest tests

.PHONY: all
all: lint mypy test

.PHONY: docs
docs:
	sphinx-build docs docs/_build
