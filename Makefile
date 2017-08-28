SHELL := /bin/bash
VIRTUALENV_DIR = $(PWD)/.venv
PIP_CMD = $(VIRTUALENV_DIR)/bin/pip
PYTEST_CMD = $(VIRTUALENV_DIR)/bin/py.test

.DEFAULT_GOAL = help

.PHONY: help
help:
        @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean:  # Cleans the environment
	rm -rf $(VIRTUALENV_DIR)

.PHONY: env
env:  ## Setups the virtualenv
	virtualenv $(VIRTUALENV_DIR)
	$(PIP_CMD) install -r requirements.txt -r requirements-dev.txt

.PHONY: test
test:  ## Runs test suite
	$(PYTEST_CMD) --cov asylum --cov-report term-missing
