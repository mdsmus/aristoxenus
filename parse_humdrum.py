#!/usr/bin/env python2.6

from __future__ import print_function
from __future__ import absolute_import, division
import re

## classes definitions


class Score():
    def append(self, item):
        self.data.append(item)

    def __init__(self):
        self.title = ""
        self.composer = ""
        self.data = []
        self.filename = ""
        self.spine_number = 0
        self.spine_types = []


class Record():
    def __repr__(self):
        return "#<Record>"

    def __init__(self, name, data):
        self.name = name
        self.data = data


class Comment():
    def __repr__(self):
        return "#<Comment>"

    def __init__(self, data):
        self.data = data


class Tandem():
    def __repr__(self):
        return "#<*" + self.type + ">"

    def __init__(self, type, data):
        self.type = type
        self.data = data


class ExclusiveInterpretation():
    def __repr__(self):
        return "#<**" + self.name + ">"

    def __init__(self, name):
        self.name = name


class Note():
    def __init__(self):
        self.name = name
        self.duration = None
        self.articulations = []
        self.beams = []
        self.octave = None
        self.code = None
        self.system = "base40"
        self.type = ""


class Bar():
    def __repr__(self):
        return "#<Bar " + self.number + ">"

    def __init__(self, number, repeat_begin=False,
                 repeat_end=False, double=False):
        self.number = number or ""
        self.repeat_begin = repeat_begin
        self.repeat_end = repeat_end
        self.double = double


class Rest():
    def __init__(self):
        self.duration = None
        self.print_as_whole = False


class NullToken():
    def __repr__(self):
        return "#<.>"


## Utilities


def regexp(reg, string):
    tmp = re.search(reg, string)
    if tmp:
        return tmp.group()


## parse humdrum types


def parse_kern(string, line_number, item_number):
    return string


def parse_dynam(string, line_number, item_number):
    return string


def unknown_data_type(item, line_number, item_number):
    return item


## parse elements


def parse_bar(string):
    repeat_begin = regexp(":\\||:!", string)
    repeat_end = regexp("\\|:|!:", string)
    double = regexp("==", string)
    number = regexp("[0-9]+([a-z]+)?", string)

    return Bar(number, repeat_begin, repeat_end, double)


def parse_tandem(string):
    return Tandem(string, None)


def parse_data(item, line_number, item_number, data_type):
    dic = {"kern": parse_kern,
           "dynam": parse_dynam}

    return dic.get(data_type, unknown_data_type)(item, line_number, item_number)


## basic parser


def parse_spine_item(item, line_number, item_number, score):
    if item.startswith("="):
        return parse_bar(item)
    elif item.startswith("**"):
        spine_type = item[2:]
        score.spine_types.append(spine_type)
        return ExclusiveInterpretation(spine_type)
    elif item.startswith("*"):
        return parse_tandem(item)
    elif item.startswith("!"):
        return Comment(item[1:])
    elif item == ".":
        return NullToken()
    else:
        data_type = score.spine_types[item_number]
        return parse_data(item, line_number, item_number, data_type)


def parse_reference_record(line):
    s = line.split(":", 1)
    return Record(s[0][3:], s[1])


def parse_global_comment(line):
    return Comment(line)


def parse_spine(line, line_number, score):
    list = []
    item_number = 0
    for item in line.split("\t"):
        list.append(parse_spine_item(item, line_number, item_number, score))
        item_number += 1
    return(list)


def parse_humdrum_file(file):
    blank_line = re.compile("^[ \t]*$")
    reference_record = re.compile("^!{3,3}[a-zA-Z ]+")
    global_comment = re.compile("^(!{2,2})|(!{4})[a-zA-Z ]+")

    line_number = 0
    score = Score()

    with open(file) as f:
        for line in f.read().split('\n'):
            line_number += 1
            if blank_line.match(line):
                score.append("")
            elif reference_record.match(line):
                score.append(parse_reference_record(line))
            elif global_comment.match(line):
                score.append(parse_global_comment(line))
            else:
                score.append(parse_spine(line, line_number, score))
        return score

## test usage

f = parse_humdrum_file("/home/kroger/Documents/xenophilus/test.krn")
#f = parse_humdrum_file("/home/kroger/Documents/xenophilus/k160-02.krn")
for item in f.data:
    print(item)
