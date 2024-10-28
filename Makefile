VE ?= ./ve
REQUIREMENTS ?= requirements.txt
SYS_PYTHON ?= python3
PY_SENTINAL ?= $(VE)/sentinal
PIP_VERSION ?= 24.3.1
MAX_COMPLEXITY ?= 10
PY_DIRS ?= $(APP)
FLAKE8 ?= $(VE)/bin/flake8
PIP ?= $(VE)/bin/pip

$(PY_SENTINAL): $(REQUIREMENTS)
	rm -rf $(VE)
	$(SYS_PYTHON) -m venv $(VE)
	$(PIP) install pip==$(PIP_VERSION)
	$(PIP) install --no-deps --requirement $(REQUIREMENTS)
	touch $@

flake8: $(PY_SENTINAL)
	$(FLAKE8) $(PY_DIRS) --max-complexity=$(MAX_COMPLEXITY) --exclude=*/local_settings.py,*/migrations/*.py,ve --extend-ignore=$(FLAKE8_IGNORE)

clean:
	rm -rf $(VE)
	rm .DS_Store
	rm -rf __pycache__

process: $(PY_SENTINAL)
	$(VE)/bin/python3 process.py

.PHONY: check flake8 sanitize process clean
