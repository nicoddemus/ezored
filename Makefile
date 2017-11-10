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
	@echo "- deps"
	@echo "- clean"
	@echo ""

install:
	pip install -e .[test]

test:
	python setup.py test

deps:
	pip install -r requirements.txt

clean:
	find . -regex "\(.*__pycache__.*\|*.py[co]\)" -delete
	find . -type d -name __pycache__ -exec rm -r {} \+
