install:
	poetry install

dev:
	poetry run python manage.py runserver

PORT ?= 8000
start:
	python3 manage.py migrate
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

lint:
	poetry run flake8 --ignore=E501 task_manager

test:
	poetry run python manage.py test --verbosity 2

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage xml

selfcheck:
	poetry check

check: selfcheck test lint