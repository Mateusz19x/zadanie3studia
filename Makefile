.PHONY: install run test lint format clean help

help:
	@echo "Mailer Project - Available Commands"
	@echo ""
	@echo "  make install    - Install dependencies in virtual environment"
	@echo "  make run        - Start the Flask application"
	@echo "  make test       - Run the test suite"
	@echo "  make lint       - Run pylint linting"
	@echo "  make format     - Format code with black"
	@echo "  make clean      - Remove cache and temporary files"
	@echo ""

install:
	pip install -r requirements.txt

run:
	python web.py

test:
	python -m pytest -v --tb=short

lint:
	python -m pylint subscribers.py email_sender.py web.py __init__.py

format:
	python -m black subscribers.py email_sender.py web.py __init__.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov .pylint.d
