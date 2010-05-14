#!/usr/bin/env python

import optparse

from aristoxenus import parse
from aristoxenus import emit
from aristoxenus import score

def extract_field(opt, sco):
    data = sco.get_spine(int(opt))
    print emit.humdrum.show(score.Score(*data))

def extract_interpretation(opt, sco):
    pass

def extract_spinepath(opt, sco):
    pass

def extract_trace(opt, sco):
    pass


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", "--field", help="field mode",
                      action="store", dest="field")
    parser.add_option("-i", "--interpretation", help="interpretation mode",
                      action="store", dest="interpretation")
    parser.add_option("-p", "--spine-path", help="spine path mode",
                      action="store", dest="spinepath")
    parser.add_option("-t", "--trace", help="field-trace mode",
                      action="store", dest="trace")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("I need at least one file.")

    for fname in args:
        sco = parse.humdrum.parse_file(fname)
        if options.field:
            extract_field(options.field, sco)
        elif options.interpretation:
            extract_interpretation(options.interpretation, sco)
        elif options.spinepath:
            extract_spinepath(options.spinepath, sco)
        elif options.trace:
            extract_trace(options.trace, sco)
