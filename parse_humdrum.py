#!/usr/bin/env python2.6

from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division
import re
import sys

## classes definitions


class Base(object):
    repr = ''

    def space(self):
        if self.repr:
            return ' '
        else:
            return ''

    def __repr__(self):
        return "<" + self.__class__.__name__ + self.space() + self.repr + ">"


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
    def __init__(self, type, data):
        self.type = type
        self.data = data
        self.repr = type


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


class MultipleStop(list):
    def __repr__(self):
        return '<MS: ' + str(self.__getslice__(0,self.__sizeof__())) + '>'


class Bar(Base):
    def __init__(self, number, repeat_begin=False,
                 repeat_end=False, double=False):
        self.number = number or ""
        self.repeat_begin = repeat_begin
        self.repeat_end = repeat_end
        self.double = double
        self.repr = self.number


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


def isPython3():
    return sys.version[:1] == '3'

def isMatch(reg, string):
    tmp = re.search(reg, string)
    if tmp:
        return tmp.group()


## Parse kern

kern_articulations = {
    'n': "natural", '/': "up-stem", '\\': "down-stem", 'o': "harmonic",
    't': "trill-st", 'T': "trill-wt", 'S': "turn", '$': "inverted-turn",
    'R': "end-with-turn", 'u': "down-bow", 'v': "up-bow", 'z': "sforzando",
    'H': "glissando-start", 'h': "glissando-end", ';': "fermata", 'Q': "gruppetto",
    'p': "appoggiatura-main-note", 'U': "mute", '[': "tie-start", ']': "tie-end",
    '_': "tie-midle", '(': "slur-start", ')': "slur-end", '{': "phrase-start",
    '}': "phrase-end", '\'': "staccato", 's': "spiccato", '\\': "pizzicato", 
    '`': "staccatissimo", '~': "tenuto", '^': "accent", ':': "arpeggiation",
    ',': "breath", 'm': "mordent-st", 'w': "inverted-mordent-st", 'M': "mordent-wt",
    'W': "inverted-mordent-wt"
}

kern_beams = {
    'L': 'beam-start',
    'J': 'beam-end',
    'K': 'beam-partial-right',
    'k': 'beam-partial-left'
    }


def findChar(char, string):
    if string.find(char) >= 0:
        return True
    else:
        return False


def isDuration(char):
    return findChar(char, "0123456789")


def isNote(char):
    return findChar(char, "abcdefg")


def isDot(char):
    return char == '.'

def isAccidental(char):
    return findChar(char, "#-")

def isArticulation(char):
    return char in kern_articulations


def isBeam(char):
    return char in kern_beams


def isRest(char):
    return char == 'r'


def isAcciacatura(char):
    return char == 'q'


def isAppoggiatura(char):
    return char == 'P'


def ParseChar(char, dic, var, msg, cond):
    if cond:
        dic[var].append(char)
    else:
        raise KernError(msg)


def prev_string(string, i):
    previous = i - 1
    if previous < 0:
        return ''
    else:
        return string[previous]
            
def kern_tokenizer(string, linen):
    dic = {'durs': [], 'notes': [], 'rests': [], 'articulations': [], 
           'beams': [], 'acciaccatura': [], 'appoggiatura': []}

    for i in range(0, len(string)):
        pchar = prev_string(string, i)
        char = string[i]

        if isDuration(char):
            ParseChar(char, dic, 'durs', "Duration must be together.",
                      (pchar == '' or dic['durs'] == [] or isDuration(pchar)))
        elif isNote(char):
            ParseChar(char, dic, 'notes', "Notes must be together.",
                      (pchar == '' or dic['notes'] == [] or isNote(pchar)))
        elif isDot(char):
            ParseChar(char, dic, 'dots', "Dots must be together or after a number."
                      (isDuration(pchar) or isDot(pchar)))
        elif isAccidental(char):
            ParseChar(char, dic, 'accidentals', "Accidentals."
                      (isNote(pchar) or (isAccidental(pchar) and char == pchar)))
        elif isRest(char):
            ParseChar(char, dic, 'rests', "Rest."
                      (isRest(pchar) or dic['rests'] == ''))
        elif isAppoggiatura(char):
            ParseChar(char, dic, 'appoggiatura', "Appoggiatura"
                      (dic['notes'] and dic['durs']))
        elif isArticulation(char):
            dic['articulations'] = kern_articulations[char]
        elif isBeam(char):
            dic['beams'] = kern_beams[char]
        elif isAcciacatura(char):
            dic['acciaccatura'] = char
        else:
            print("Humdrum character not recognized: " + char)
    print(dic)
    return dic


def parse_kern_item(string, lineno, item_number):
    kern_tokenizer(string, lineno)
    return string


def parse_kern(string, linen, itemn):
    s = string.split(" ")
    if not string:
        raise KernError("Kern string shoudn't be empty.")
    elif len(s) == 1:
        return parse_kern_item(string, linen, itemn)
    else:
        return MultipleStop([parse_kern_item(item, linen, itemn) for item in s])


## Parse dynam

def parse_dynam(string, line_number, item_number):
    return string


## parse elements

def unknown_type(item, line_number, item_number):
    return item


def parse_bar(string):
    repeat_begin = isMatch(":\\||:!", string)
    repeat_end = isMatch("\\|:|!:", string)
    double = isMatch("==", string)
    number = isMatch("[0-9]+([a-z]+)?", string)

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
            if isMatch(r"^[ \t]*$", line) is not None:
                score.append(BlankLine())
            elif isMatch(r"^!{3}[a-zA-Z ]+", line):
                score.append(parse_reference_record(line))
            elif isMatch(r"^(!{2})|(!{4,})[a-zA-Z ]+", line):
                score.append(parse_global_comment(line))
            else:
                score.append(parse_spine(line, line_number, score))
        return score

## test usage

f = parse_humdrum_file("/home/kroger/Documents/xenophilus/data/test.krn")
#f = parse_humdrum_file("/home/kroger/Documents/xenophilus/k160-02.krn")
for item in f.data: print(item)
