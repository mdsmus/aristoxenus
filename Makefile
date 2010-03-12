test:
	./tests.py

check:
	./tools/pep8.py *.py

clean:
	rm -f *.out parsetab.py

print: humdrum.ps

%.ps: %.py
	a2ps -o $@ $<
