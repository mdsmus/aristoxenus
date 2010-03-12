all: test check coverage

test:
	./tests.py

check:
	./tools/pep8.py *.py

coverage:
	coverage run humdrum.py
	coverage html

clean:
	rm -f *.out parsetab.py

print: humdrum.ps

%.ps: %.py
	a2ps -o $@ $<
