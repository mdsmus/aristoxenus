#!/usr/bin/env python2.6

from __future__ import print_function
from __future__ import absolute_import, division
import re


class Score():
    def __init__(self):
        self.title = ""
        self.composer = ""
        self.data = []
        self.filename = ""
        self.spine_number = 0


def parse_global_comment(line):
    print("global comment")


def parse_reference_record(line):
    print("reference_record")


def parse_spine(line):
    line


def parse_humdrum_file(file):
    blank_line = re.compile("^[ \t]*$")
    reference_record = re.compile("^!{3,3}[a-zA-Z ]+")
    global_comment = re.compile("^(!{2,2})|(!{4})[a-zA-Z ]+")
    local_comment = re.compile("^!{1,1}[a-zA-Z ]+")

    line_number = 0
    score = Score()

    with open(file) as f:
        for line in f.read().split('\n'):
            line_number += 1
            if blank_line.match(line):
                ""
            elif reference_record.match(line):
                parse_reference_record(line)
            elif global_comment.match(line):
                parse_global_comment(line)
            else:
                parse_spine(line)
        return score

f = parse_humdrum_file("/home/kroger/Documents/xenophilus/test.krn")
print(f.data)
