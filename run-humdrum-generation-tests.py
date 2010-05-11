#!/usr/bin/env python

import os
from difflib import SequenceMatcher
from aristoxenus import humdrum
from aristoxenus import convert


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
        conversion = convert.show_as_humdrum(humdrum.parse_file(filename))
        s = SequenceMatcher(None, kernfile, conversion)
        ratio = s.ratio()

        print "- {0:35}".format(filename),

        if ratio == 1.0:
            print_color(ratio, "green")
        else:
            print_color(ratio, "red")


def run_datatest():
    ok = 0
    errors = 0

    for fname in os.listdir("datatest"):
        fullname = os.path.join("datatest", fname)
        try:
            compare_humdrum_file(fullname)
            ok += 1
        except:
            print "- {0:35} [error]".format(fullname)
            errors += 1

    print "\nI ran {0} files, where ok: {1} and errors: {2}".format(ok + errors, ok, errors)


run_datatest()
