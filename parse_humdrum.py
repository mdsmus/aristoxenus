#!/usr/bin/env python2.6

from __future__ import print_function
from __future__ import absolute_import, division
import re
import pyparsing

## classes definitions


class Base(object):
    def __repr__(self):
        return "<" + self.__class__.__name__ + ">"


class Score(Base):
    def append(self, item):
        self.data.append(item)

    def __init__(self):
        self.title = ""
        self.composer = ""
        self.data = []
        self.filename = ""
        self.spine_number = 0
        self.spine_types = []


class Record(Base):
    def __init__(self, name, data):
        self.name = name
        self.data = data


class Comment(Base):
    def __init__(self, data):
        self.data = data


class Tandem(Base):
    def __repr__(self):
        return "<*" + self.type + ">"

    def __init__(self, type, data):
        self.type = type
        self.data = data


class ExclusiveInterpretation(Base):
    def __repr__(self):
        return "<**" + self.name + ">"

    def __init__(self, name):
        self.name = name


class Note(Base):
    def __init__(self):
        self.name = name
        self.duration = None
        self.articulations = []
        self.beams = []
        self.octave = None
        self.code = None
        self.system = "base40"
        self.type = ""


class Bar(Base):
    def __repr__(self):
        return "<Bar " + self.number + ">"

    def __init__(self, number, repeat_begin=False,
                 repeat_end=False, double=False):
        self.number = number or ""
        self.repeat_begin = repeat_begin
        self.repeat_end = repeat_end
        self.double = double


class Rest(Base):
    def __init__(self):
        self.duration = None
        self.print_as_whole = False


class NullToken(Base):
    pass


class BlankLine(Base):
    pass


## Exceptions

class KernError(Exception):
    pass


## Utilities


def regexp(reg, string):
    tmp = re.search(reg, string)
    if tmp:
        return tmp.group()


## Parse kern

kern_articulations = {
    'n': "natural",
    '/': "up-stem",
    '\\': "down-stem",
    'o': "harmonic",
    't': "trill-st",
    'T': "trill-wt",
    'S': "turn",
    '$': "inverted-turn",
    'R': "end-with-turn",
    'u': "down-bow",
    'v': "up-bow",
    'z': "sforzando",
    'H': "glissando-start",
    'h': "glissando-end",
    ';': "fermata",
    'Q': "gruppetto",
    'p': "appoggiatura-main-note",
    'U': "mute",
    '[': "tie-start",
    ']': "tie-end",
    '_': "tie-midle",
    '(': "slur-start",
    ')': "slur-end",
    '{': "phrase-start",
    '}': "phrase-end",
    '\'': "staccato",
    's': "spiccato",
    '\\': "pizzicato", 
    '`': "staccatissimo",
    '~': "tenuto",
    '^': "accent",
    ':': "arpeggiation",
    ',': "breath",
    'm': "mordent-st",
    'w': "inverted-mordent-st",
    'M': "mordent-wt",
    'W': "inverted-mordent-wt"}


def kern_tokenizer(string, linen):
    return string


def parse_kern_item(string, line_number, item_number):
    return string


def parse_kern(string, linen, itemn):
    s = string.split(" ")
    if not string:
        raise KernError("Kern string shoudn't be empty.")
    elif len(s) == 1:
        return parse_kern_item(string, linen, itemn)
    else:
        return [parse_kern_item(item, linen, itemn) for item in s]


## Parse dynam

def parse_dynam(string, line_number, item_number):
    return string


## parse elements

def unknown_type(item, line_number, item_number):
    return item


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

    return dic.get(data_type, unknown_type)(item, line_number, item_number)


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
    line_number = 0
    score = Score()

    with open(file) as f:
        for line in f.read().split('\n'):
            line_number += 1
            if regexp(r"^[ \t]*$", line) is not None:
                score.append(BlankLine())
            elif regexp(r"^!{3}[a-zA-Z ]+", line):
                score.append(parse_reference_record(line))
            elif regexp(r"^(!{2})|(!{4,})[a-zA-Z ]+", line):
                score.append(parse_global_comment(line))
            else:
                score.append(parse_spine(line, line_number, score))
        return score

## test usage

f = parse_humdrum_file("/home/kroger/Documents/xenophilus/test.krn")
#f = parse_humdrum_file("/home/kroger/Documents/xenophilus/k160-02.krn")
for item in f.data:
    print(item)
