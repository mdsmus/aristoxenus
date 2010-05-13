PROJNAME = aristoxenus
export PYTHONPATH=$(CURDIR)/$(PROJNAME)

PYTHONFILES = $(wildcard $(PROJNAME)/*.py)
LINT_ARGS = --min-public-methods=0 --include-ids=y --max-attributes=9

.PHONY: docs tests

all: humdrum check

lint:
	pylint $(LINT_ARGS) $(PROJNAME)

check:
	./tools/pep8.py $(PROJNAME)/*.py

tests:
	py.test --tb=line

test-all: test-compositions test-data

test-compositions:
	./humdiff compositions/*/*.krn

test-data:
	./humdiff data/*.krn

docs:
	cd docs; $(MAKE) html

profile:
	python -m "profile" $(PROJNAME)/*.py

metrics:
	pymetrics aristoxenus/*.py

coverage:
	coverage run --branch $(PROJNAME)/humdrum.py
	coverage report

callgraph:
	pycallgraph ./run-interactive.py -i aristoxenus.* -e *.*

TAGS: $(PYTHONFILES)
	find /usr/lib/python2.6/ . -name "*.py" | etags --output TAGS -

clean:
	find -name "*.pyc" | xargs rm
	rm -rf *.out parsetab.py htmlcov
