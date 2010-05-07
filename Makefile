PROJNAME = aristoxenus
export PYTHONPATH=$(CURDIR)/$(PROJNAME)

PYTHONFILES = $(wildcard $(PROJNAME)/*.py)
LINT_ARGS = --min-public-methods=0 --include-ids=y --max-attributes=9

.PHONY: docs tests

all: humdrum check

lint:
	pylint $(LINT_ARGS) $(PROJNAME)/*.py

parse:
	./parse_files.py

docs:
	cd doc; $(MAKE) html

tests:
	py.test --tb=line

profile:
	python -m "profile" $(PROJNAME)/*.py

check:
	./tools/pep8.py $(PROJNAME)/*.py

coverage:
	coverage run --branch $(PROJNAME)/humdrum.py
	coverage report

TAGS: $(PYTHONFILES)
	find /usr/lib/python2.6/ . -name "*.py" | etags --output TAGS -

clean:
	find -name "*.pyc" | xargs rm
	rm -rf *.out parsetab.py htmlcov
