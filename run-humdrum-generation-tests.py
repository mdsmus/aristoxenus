#!/usr/bin/env python

import os
from difflib import SequenceMatcher
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
        kernfile = f.read()
        conversion = emit.humdrum.show(parse.humdrum.parse_file(filename))
        s = SequenceMatcher(None, kernfile, conversion)
        ratio = s.ratio()

        print "- {0:35}".format(filename),

        if ratio == 1.0:
            print_color(ratio, "green")
        else:
            print_color(ratio, "red")

        return ratio


def run_datatest():
    noerrors = 0
    errors = 0
    good = 0
    bad = 0

    files = os.listdir("datatest")
    files.sort()

    for fname in files:
        fullname = os.path.join("datatest", fname)
        try:
            ratio = compare_humdrum_file(fullname)
            if ratio == 1:
                good += 1
            else:
                bad += 1
            noerrors += 1
        except:
            print "- {0:35} [error]".format(fullname)
            errors += 1

    print "\n{0} files, no errors: {1}, errors: {2}".format(noerrors + errors, noerrors, errors)
    print "bottom line: good: {0}, bad: {1}".format(good, bad)
    print

run_datatest()
