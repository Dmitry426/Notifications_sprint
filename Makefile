.PHONY: dev pre-commit isort black mypy flake8 pylint lint

dev: pre-commit

pre-commit:
	pre-commit install
	pre-commit autoupdate

isort:
	isort . --profile black

black:
	black .

mypy:
	mypy -p workers

flake8:
	flake8 .

pylint:
	pylint workers

lint: isort black mypy flake8 pylint
