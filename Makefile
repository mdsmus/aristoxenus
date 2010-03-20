PYTHON_FILES = $(wildcard xenophilus/*.py)

all: runexample check #coverage

tests:
	nosetests

runexample:
	./example

check:
	./tools/pep8.py *.py

coverage:
	coverage run xenophilus/humdrum.py
	coverage html

TAGS: $(PYTHON_FILES)
	find /usr/lib/python2.6/ . -name "*.py" | etags --output TAGS -

clean:
	rm -f *.out parsetab.py

print: humdrum.ps

%.ps: %.py
	a2ps -o $@ $<
