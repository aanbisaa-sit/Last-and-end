# Makefile — Last and End

.PHONY: test lint typecheck format install clean all coverage

SHELL := /bin/bash
PY := python3
PIP := pip3

# Create .venv if it does not exist yet.
VENV := .venv
$(VENV): requirements-dev.txt
	$(PY) -m venv $@
	$($(VENV)/bin/pip) install -r $<

# Default target: format + lint + typecheck + test.
all: format lint typecheck test

install:
	$(PIP) install -e . 2>/dev/null || $(PIP) install .
	$(PIP) install pytest mypy ruff

# ── tests ─────────────────────────────────────────────────────────────────────
test:
	$(PY) -m pytest tests/ -v

test-cov: $(VENV)
	$($(VENV)/bin/pytest) tests/ --cov=src/last_and_end --cov-report=term-missing

coverage: test-cov

# ── lint / typecheck ──────────────────────────────────────────────────────────
lint:
	ruff check src/last_and_end tests/

lint-fix:
	ruff check --fix src/last_and_end tests/

typecheck: $(VENV)
	$($(VENV)/bin/mypy) src/last_and_end/

# ── format ────────────────────────────────────────────────────────────────────
format:
	ruff format src/last_and_end tests/

# ── run tracker ───────────────────────────────────────────────────────────────
run:
	$(PY) -m last_and_end --config config.example.toml

# ── clean ─────────────────────────────────────────────────────────────────────
clean:
	rm -rf .venv/
	rm -rf dist/ build/ *.egg-info/
	rm -rf .coverage htmlcov/ .mypy_cache/ .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# ── build ─────────────────────────────────────────────────────────────────────
build:
	$(PY) -m build

publish: build
	$(PY) -m twine upload dist/*
