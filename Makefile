# Makefile — Last and End

.PHONY: test lint typecheck format install clean all

SHELL := /bin/bash
PY := python3
PIP := pip3

# Default target: run everything useful in development order.
all: format lint typecheck test

# ── install ───────────────────────────────────────────────────────────────────
install:
	$(PIP) install -e ".[dev]" 2>/dev/null || $(PIP) install -e .
	$(PIP) install pytest mypy ruff

# ── tests ─────────────────────────────────────────────────────────────────────
test:
	$(PY) -m pytest tests/ -v

test-cov:
	$(PY) -m pytest tests/ --cov=src/last_and_end --cov-report=term-missing

# ── lint / typecheck ──────────────────────────────────────────────────────────
lint:
	ruff check src/last_and_end tests/

lint-fix:
	ruff check --fix src/last_and_end tests/

typecheck:
	mypy src/last_and_end/

# ── format ────────────────────────────────────────────────────────────────────
format:
	ruff format src/last_and_end tests/

# ── run tracker ───────────────────────────────────────────────────────────────
run:
	$(PY) -m last_and_end --config config.example.toml

# ── clean ─────────────────────────────────────────────────────────────────────
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -f .coverage htmlcov/ .mypy_cache/ .ruff_cache/
	rm -rf dist/ build/ *.egg-info/
