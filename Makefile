.PHONY: install layer serve

install:
	npm install
	poetry install

layer:
	rm -rf lambda/layer/python
	mkdir -p lambda/layer/python
	poetry export --only main -f requirements.txt --without-hashes | \
		pip install -r /dev/stdin -t lambda/layer/python

lint:
	poetry run black app
	poetry run isort app

lint-check:
	poetry run black --check app
	poetry run isort --check-only app
