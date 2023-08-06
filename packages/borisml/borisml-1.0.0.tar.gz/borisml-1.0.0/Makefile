.PHONY: clean clean-build clean-pyc clean-out docs help
.DEFAULT_GOAL := help

clean: clean-build clean-pyc

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove python file artifacts
	find . -name '__pycache__' -exec rm -fr {} +

lint: ## check style with flake8
	flake8 boris

dist: clean # build source and wheel package
	python setup.py sdist bdist_wheel
	ls -l dist

install: clean # install the package to active site
	pip install .

uninstall: clean
	pip uninstall borisml
