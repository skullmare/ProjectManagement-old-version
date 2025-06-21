lint:
    flake8 .
    pylint --load-plugins pylint_django your_project_name apps
    black --check .
    isort --check-only .

format:
    black .
    isort .