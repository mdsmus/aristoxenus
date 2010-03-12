#!/usr/bin/env python2.6

from __future__ import print_function
from __future__ import absolute_import, division
import re
import math
import operator
from collections import defaultdict
from fractions import Fraction
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
    def __init__(self, spine_type, data):
        self.type = spine_type
        self.data = data
        self.repr = spine_type


class ExclusiveInterpretation(Base):
    def __repr__(self):
        return "<**" + self.name + ">"

    def __init__(self, name):
        self.name = name


class Note(Base):
    def __init__(self, name, dur, art, beams, octave, code, system, spinetype):
        print("------>", name, dur, art, beams, octave, code, system, spinetype)
        self.name = name
        self.duration = dur
        self.articulations = art
        self.beams = art
        self.octave = octave
        self.code = code
        self.system = system
        self.type = spinetype
        self.repr = "{0}{1}".format(name, dur)


class MultipleStop(list):
    def __repr__(self):
        return '<MS: ' + str(self.__getslice__(0, self.__sizeof__())) + '>'


class Bar(Base):
    def __init__(self, number, repeat_begin=False,
                 repeat_end=False, double=False):
        self.number = number or ""
        self.repeat_begin = repeat_begin
        self.repeat_end = repeat_end
        self.double = double
        self.repr = self.number


class Rest(Base):
    def __init__(self, dur, wholeNote=False):
        self.duration = dur
        self.print_as_whole = wholeNote
        self.repr = "{0}".format(dur)


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


def find_char(char, string):
    if string.find(char) >= 0:
        return True
    else:
        return False


## Parse kern

kern_articulations = {
    'n': "natural", '/': "up-stem", '\\': "down-stem", 'o': "harmonic",
    't': "trill-st", 'T': "trill-wt", 'S': "turn", '$': "inverted-turn",
    'R': "end-with-turn", 'u': "down-bow", 'v': "up-bow", 'z': "sforzando",
    'H': "glissando-start", 'h': "glissando-end", ';': "fermata",
    'Q': "gruppetto", 'p': "appoggiatura-main-note", 'U': "mute",
    '[': "tie-start", ']': "tie-end", '_': "tie-midle",
    '(': "slur-start", ')': "slur-end", '{': "phrase-start",
    '}': "phrase-end", '\'': "staccato", 's': "spiccato", '\\': "pizzicato",
    '`': "staccatissimo", '~': "tenuto", '^': "accent", ':': "arpeggiation",
    ',': "breath", 'm': "mordent-st", 'w': "inverted-mordent-st",
    'M': "mordent-wt", 'W': "inverted-mordent-wt"}

kern_beams = {
    'L': 'beam-start',
    'J': 'beam-end',
    'K': 'beam-partial-right',
    'k': 'beam-partial-left'}


def isDuration(char):
    return find_char(char, "0123456789")


def isNote(char):
    return find_char(char, "abcdefgABCDEFG")


def isDot(char):
    return char == '.'


def isAccidental(char):
    return find_char(char, "#-")


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


def parse_char(char, dic, var, msg, cond):
    if cond:
        return dic[var].append(char)
    else:
        raise KernError(msg)


def parse_kern_note(note, accidentals, lineno):
    return note[0].lower() + "".join(accidentals).replace("-", "b")


def parse_kern_octave(note, lineno):
    n = note[0]
    if n.islower:
        return 3 + len(note)
    else:
        value = [3, 2, 1, 0][note[-1]]
        if value:
            return value
        else:
            raise KernError("Octave is too low.")


def sum_power(start, end):
    return reduce(operator.add, [pow(2, x) for x in range(start, end - 1, -1)])


## FIXME to work with fractions
def calculate_duration(durs, dots):
    d = int("".join(durs))
    duration = Fraction(1, 2) if d == 0 else d
    max = math.floor(math.log(duration, 2)) * -1
    min = max - len(dots)
    return sum_power(min, max)


def string_to_code(note_name, code):
    base40 = [None,
              "cbb", "cb", "c", "c#", "c##", None,
              "dbb", "db", "d", "d#", "d##", None,
              "ebb", "eb", "e", "e#", "e##",
              "fbb", "fb", "f", "f#", "f##", None,
              "gbb", "gb", "g", "g#", "g##", None,
              "abb", "ab", "a", "a#", "a##", None,
              "bbb", "bb", "b", "b#", "b##"]

    dic = {'base40': base40}

    return dic[code].index(note_name)


def prev_string(string, i):
    previous = i - 1
    if previous < 0:
        return ''
    else:
        return string[previous]


def kern_tokenizer(string, linen):
    dic = defaultdict(list)

    for i in range(0, len(string)):
        pchar = prev_string(string, i)
        char = string[i]

        if isDuration(char):
            parse_char(char, dic, 'durs', "Duration must be together.",
                       (not pchar or not dic['durs'] or isDuration(pchar)))
        elif isNote(char):
            parse_char(char, dic, 'notes', "Notes must be together.",
                       (not pchar or not dic['notes'] or isNote(pchar)))
        elif isDot(char):
            parse_char(char, dic, 'dots', "Dots must be together or after a number.",
                       (isDuration(pchar) or isDot(pchar)))
        elif isAccidental(char):
            parse_char(char, dic, 'accidentals', "Accidentals.",
                       (isNote(pchar) or (isAccidental(pchar) and char == pchar)))
        elif isRest(char):
            parse_char(char, dic, 'rests', "Rest.",
                       (isRest(pchar) or not dic['rests']))
        elif isAppoggiatura(char):
            parse_char(char, dic, 'appoggiatura', "Appoggiatura",
                       (dic['notes'] and dic['durs']))
        elif isArticulation(char):
            dic['articulations'].append(kern_articulations[char])
        elif isBeam(char):
            dic['beams'].append(kern_beams[char])
        elif isAcciacatura(char):
            dic['acciaccatura'].append(char)
        else:
            print("Humdrum character not recognized: " + char)
    return dic


def parse_kern_item(string, lineno, item_number):
    dic = kern_tokenizer(string, lineno)
    if (not dic['durs']) and ((not dic['acciaccatura']) or (not dic['appoggiatura'])):
        raise KernError("Duration can't be NULL.")

    if (dic['notes'] and dic['rests']):
        raise KernError("A note can't have a pitch and a rest.")

    if dic['notes']:
        name = parse_kern_note(dic['notes'], dic['accidentals'], lineno)
        octave = parse_kern_octave(name, lineno)
        # FIXME
        #dur = calculate_duration(dic['durs'], dic['dots'])
        dur = dic['durs']
        code = string_to_code(name, "base40")
        return Note(name, dur, dic['articulations'], dic['beams'], octave,
                    code, "base40", "kern")
    elif dic['rests']:
        # FIXME
        #dur = calculate_duration(dic['durs'], dic['dots'])
        dur = dic['durs']
        if dic['rests'] or len(dic['rests']) >= 1:
            wholeNote = False
        else:
            wholeNote = True

        return Rest(dur, wholeNote)
    else:
        raise KernError("Kern data must have a note or rest.")


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
    return Bar(isMatch("[0-9]+([a-z]+)?", string),
               isMatch(":\\||:!", string),
               isMatch("\\|:|!:", string),
               isMatch("==", string))


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

def test():
    #f = parse_humdrum_file("/home/kroger/Documents/xenophilus/data/k160-02.krn")
    f = parse_humdrum_file("/home/kroger/Documents/xenophilus/data/test.krn")
    for item in f.data: print(item)
