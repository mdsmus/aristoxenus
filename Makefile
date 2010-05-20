PROJNAME = aristoxenus
export PYTHONPATH=$(CURDIR)/$(PROJNAME)

PYTHONFILES = $(shell find $(PROJNAME) -name "*.py")
LINT_ARGS = --min-public-methods=0 --include-ids=y --max-attributes=9

.PHONY: docs tests coverage

all: tests

lint:
	pylint $(LINT_ARGS) $(PROJNAME)

check:
	@./tools/pep8.py $(PYTHONFILES)

# run test-unit and test-data
tests:
	tools/run-tests

test-unit:
	py.test --tb=line --cover=aristoxenus --cover-report=report

test-data:
	./humdiff data/*.krn

coverage-html:
	py.test --tb=line --cover=aristoxenus --cover-report=html

test-compositions:
	./humdiff compositions/*/*.krn

docs:
	cd docs; $(MAKE) html

profile:
	./performance

metrics:
	pymetrics $(PYTHONFILES)

TAGS: $(PYTHONFILES)
	ctags-exuberant -e -R --languages=python --exclude="__init__.py"
#	find . -name "*.py" | xargs etags --output TAGS -l python

clean:
	find -name "*.pyc" | xargs rm -f
	rm -rf *.out parsetab.py coverage *.stats metricData.* TAGS


h: help
help:
	@echo
	@echo "tests:              run unit and integration tests"
	@echo "test-unit:          run unit tests"
	@echo "test-data:          run integration tests"
	@echo "test-compositions:  run humdiff in all files in 'compositions'"
	@echo "coverage-html:      generate coverage report in html format"
	@echo
	@echo "docs:               generate documentation"
	@echo
	@echo "check:              check files against pep8"
	@echo "lint:               run pylint"
	@echo "metrics:            run pymetrics"
	@echo "profile:            profile aristoxenus on WCT1 fugue 20"
	@echo
	@echo "TAGS:               generate tags"
	@echo "clean:              clean garbage"

# callgraph:
# 	pycallgraph ./test-interactive.py -i aristoxenus.* -e *.*

