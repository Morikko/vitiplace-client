.PHONY: tests

tests:
	pytest tests/

lint:
	flake8
	mypy .