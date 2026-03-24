.PHONY: install test lint format typecheck security build all

run:
	PYTHONPATH=src uv run terminal-solitaire

test:
	uv run pytest

lint:
	uv run ruff check src/ tests/

format:
	uv run ruff format src/ tests/

typecheck:
	uv run mypy src/

all:
	format lint typecheck test
