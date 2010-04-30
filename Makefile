PYTHON_FILES = $(wildcard *.py)

.PHONY: docs

all: humdrum check

lint:
	pylint --min-public-methods=0 --include-ids=y --max-attributes=9 *.py


docs:
	cd docs; $(MAKE) html

tests:
	py.test --tb=line
#	nosetests --with-doctest

profile:
	python -m "profile"  *.py

humdrum:
	python humdrum.py

check:
	./tools/pep8.py *.py

coverage:
	coverage run humdrum.py
	coverage html

TAGS: $(PYTHON_FILES)
	find /usr/lib/python2.6/ . -name "*.py" | etags --output TAGS -

clean:
	rm -f *.out parsetab.py *.pyc

print: humdrum.ps

%.ps: %.py
	a2ps -o $@ $<
