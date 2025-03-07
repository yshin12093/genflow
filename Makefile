# 📜 Makefile for GenFlow Project

.PHONY: install test run lint format clean

install:
	pip install -r requirements.txt  # Install dependencies

test:
	pytest tests/ -v  # Run tests

run:
	python -m src.graph_client  # Run the main app

lint:
	flake8 src/ helper/ tests/  # Check for Python linting errors

format:
	black src/ helper/ tests/  # Auto-format Python code

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +  # Clean cache
	rm -rf .pytest_cache logs/*  # Remove pytest cache & logs
