#!/usr/bin/env python

import os
import difflib
from difflib import SequenceMatcher
from optparse import OptionParser

import aristoxenus.parse as parse
import aristoxenus.emit as emit


def print_color(text, color):
    colors = {"black": "0;30",
              "blue": "0;34",
              "green": "0;32",
              "cyan": "0;36",
              "red": "0;31",
              "purple": "0;35",
              "brown": "0;33",
              "light_gray": "0;37",
              "dark_gray": "1;30",
              "light_blue": "1;34",
              "light_green": "1;32",
              "light_cyan": "1;36",
              "light_red": "1;31",
              "light_purple": "1;35",
              "yellow": "1;33",
              "white": "1;37"}

    print "\x1b[{0}m{1:2.2f}\x1b[{2}m".format(colors[color], text, colors["black"])


def compare_humdrum_file(filename):
    with open(filename) as f:
        orig = f.read()
        conv = emit.humdrum.show(parse.humdrum.parse_file(filename))
        s = SequenceMatcher(None, orig, conv)
        lines = zip(orig.splitlines(), conv.splitlines())
        diff = [(o, g) for o, g in lines if o != g]
        return s.ratio(), diff


def run_datatest(files, opt={}):
    noerrors = 0
    errors = 0
    good = 0
    bad = 0

    for fname in files:
        try:
            ratio, diff = compare_humdrum_file(fname)
            if ratio == 1:
                good += 1
            else:
                bad += 1
            noerrors += 1

            print "- {0:35}".format(fname),

            if ratio == 1.0:
                print_color(ratio, "green")
            else:
                print_color(ratio, "red")

        except IndexError:
            print "- {0:35} [error]".format(fname)
            errors += 1

    print "\n{0} files, no errors: {1}, errors: {2}".format(noerrors + errors, noerrors, errors)
    print "bottom line: good: {0}, bad: {1}".format(good, bad)
    print


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-v", "--verbose", help="show diff.", action="store_true", dest="verbose")
    (options, args) = parser.parse_args()

    run_datatest(args, options)
