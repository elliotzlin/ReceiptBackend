REQUIREMENTS?=requirements.txt

FLASK_APP='app/__init__.py'
FLASK_DEBUG?=1

DEV_PORT?=5000

.PHONY: install
install: venv_run

.PHONY: clean
clean: clean-venv clean-temp-files

.PHONY: clean-venv
clean-venv:
	rm -rf venv_run

.PHONY: clean-temp-files
clean-temp-files:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

.PHONY: start
start: venv_run
	FLASK_APP=$(FLASK_APP) FLASK_DEBUG=$(FLASK_DEBUG) flask run --host 0.0.0.0 --port $(DEV_PORT)

venv_run:
	python3 -m venv venv_run
	. venv_run/bin/activate && pip install -r $(REQUIREMENTS)
