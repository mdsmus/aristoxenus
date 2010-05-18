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
	tools/run-tests

test-unit:
	py.test --tb=line

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
	ctags-exuberant -e -R --languages=python --exclude="__init__.py"
#	find . -name "*.py" | xargs etags --output TAGS -l python

clean:
	find -name "*.pyc" | xargs rm
	rm -rf *.out parsetab.py htmlcov
