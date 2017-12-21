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
	@echo "- deps"
	@echo "- clean"
	@echo "- pip-package"
	@echo "- pip-upload"
	@echo ""

install:
	pip install -e .[test]

test:
	python setup.py test

test-cov:
	python setup.py test --codecoverage=html

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