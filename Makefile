PYTHON = python3
PIP = pip

ENV = env
REFERENCE_DIR = reference
TEST_FILES = test_client.py test_functionality.py

.PHONY: setup

setup:
	$(PYTHON) -m venv $(ENV)
	. $(ENV)/bin/activate;	\
	pip install -r requirements.txt; \
	pip install $(REFERENCE_DIR)/*.whl

check: test

# Run all unittests
# run "python3 -m unittest --help" for more options
# on how to run unit tests
test:
	$(PYTHON) -m unittest -v $(TEST_FILES)

clean-env:
	rm -rf $(ENV)
	rm -rf __pycache__
	rm -rf .pytest_cache
	@echo "Environment cleared.  Run 'make setup' again to create it."

