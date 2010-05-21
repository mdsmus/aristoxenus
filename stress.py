#!/usr/bin/env python

from __future__ import print_function
import random
import sys

import aristoxenus

def random_note():
    note = random.choice("abcdefg")
    acc = random.choice(["", "-", "--", "#", "##"])
    articulation = random.choice("n/otTS$RuHh;QpU[]_(){}\'s\\`~^vz,mwMW")
    duration = random.choice(["2", "4", "8", "16", "32", "64"])
    dot = random.choice(["", ".", ".."])
    return duration + dot + note + acc + articulation


def random_line(n):
    return "	".join([random_note() for x in range(0, n)]) + "	" + random_note()


def random_kern(filename, columns, lines):
    with open(filename, "w") as f:
        print("**kern	" * columns + "**kern", file=f)
        for x in xrange(0, lines):
            print(random_line(columns), file=f)


def parse(filename):
    return aristoxenus.parse.humdrum.parse_file(filename)


def parse_and_emit(filename):
    sco = aristoxenus.parse.humdrum.parse_file(filename)
    return aristoxenus.emit.humdrum.show(sco)


if __name__=='__main__':
    func = sys.argv[1]
    filename = sys.argv[2]

    if func == "generate":
        cols = int(sys.argv[3])
        lines = int(sys.argv[4])
        random_kern(filename, cols, lines)
    elif func == "parse":
        parse(filename)
    elif func == "emit":
        parse_and_emit(filename)
