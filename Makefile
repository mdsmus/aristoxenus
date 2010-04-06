PYTHON_FILES = $(wildcard xenophilus/*.py)

all: humdrum check

lint:
	pylint --min-public-methods=0 --include-ids=y --max-attributes=9 *.py

tests:
	nosetests

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
	rm -f *.out parsetab.py

print: humdrum.ps

%.ps: %.py
	a2ps -o $@ $<
