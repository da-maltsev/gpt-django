install-dev-deps: dev-deps
	pip-sync requirements.txt dev-requirements.txt

install-deps: deps
	pip-sync requirements.txt

deps:
	pip-compile --resolver=backtracking --output-file=requirements.txt pyproject.toml

dev-deps: deps
	pip-compile --resolver=backtracking --extra=dev --output-file=dev-requirements.txt pyproject.toml

fmt:
	ruff format backend
	ruff check backend --fix

lint:
	dotenv-linter backend/app/.env.ci
	cd backend && ./manage.py check
	ruff check backend
	cd backend && mypy

test:
	mkdir -p backend/static
	cd backend && ./manage.py makemigrations --dry-run --no-input --check
	cd backend && ./manage.py compilemessages
	cd backend && pytest --dead-fixtures
	cd backend && pytest -x
