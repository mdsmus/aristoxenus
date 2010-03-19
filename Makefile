all: test check coverage

test:
	./tests.py

check:
	./tools/pep8.py *.py

coverage:
	coverage run humdrum.py
	coverage html

TAGS:
	find /usr/lib/python2.6/ . -name "*.py" | etags --output TAGS -

clean:
	rm -f *.out parsetab.py

print: humdrum.ps

%.ps: %.py
	a2ps -o $@ $<
