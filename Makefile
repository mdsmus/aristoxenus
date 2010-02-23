check:
	./tools/pep8.py *.py

clean:
	rm -f *.out parsetab.py

print: humdrum-parser.ps

%.ps: %.py
	a2ps -o $@ $<
