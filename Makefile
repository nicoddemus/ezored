EXECUTABLE=ezored
LOG_FILE=/var/log/${EXECUTABLE}.log
PACKAGE=github.com/ezored/ezored

.DEFAULT_GOAL := help

help:
	@echo "Type: make [rule]. Available options are:"
	@echo ""
	@echo "- help"
	@echo "- install"
	@echo "- test"
	@echo "- test-cov"
	@echo "- test-on-docker"
	@echo "- deps"
	@echo "- clean"
	@echo "- pip-package"
	@echo "- pip-upload"
	@echo "- pip-send-update"
	@echo ""

install:
	pip install -e .[test]

test:
	python setup.py test

test-cov:
	python setup.py test --codecoverage=html

test-on-docker:
	docker run -it --rm -v "${PWD}":/app -w /app python:2.7.14-jessie make deps test-cov

deps:
	pip install -r requirements.txt

clean:
	find . -name "*.pyc" -exec rm -f {} \;
	find . -type d -name __pycache__ -exec rm -r {} \+
	rm -rf htmlcov
	rm -rf dist

pip-package:
	python setup.py sdist

pip-upload:
	twine upload dist/*

pip-send-update:
	rm -rf dist
	make pip-package
	make pip-upload