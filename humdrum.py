#!/usr/bin/env python2.6

from __future__ import print_function
from __future__ import absolute_import, division
from collections import defaultdict
from fractions import Fraction
import math
import operator
import sys
# import local modules:
import utils
import music
import kern

## classes definitions


class Base(object):
    repr = ''

    def space(self):
        return ' ' if self.repr else ''

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


class KernError(Exception):
    pass


def kern_error(message):
    raise KernError(message)

## Parse kern


def parse_kern_note(note, accs, lineno):
    return note[0].lower() + "".join(accs).replace("-", "b")


def parse_kern_octave(note, lineno):
    if note[0].islower:
        return 3 + len(note)
    else:
        value = [3, 2, 1, 0][note[-1]]
        return value or kern_error("Octave is too low.")


def kern_tokenizer(string, linen):
    dic = defaultdict(list)

    def _is(char, type):
        return char in kern.types[type][0]

    def parse(char, key, cond):
        dic[key].append(char) if cond else kern_error(kern.types[key][0])

    for i in range(0, len(string)):
        p = utils.prev_string(string, i)
        c = string[i]

        if _is(c, 'dur'):
            parse(c, 'dur', (not p or not dic['dur'] or _is(p, 'dur')))
        elif _is(c, 'note'):
            parse(c, 'note', (not p or not dic['note'] or _is(p, 'note')))
        elif _is(c, 'dot'):
            parse(c, 'dot', (_is(p, 'dur') or _is(p, 'dot')))
        elif _is(c, 'acc'):
            parse(c, 'acc', _is(p, 'note') or (_is(p, 'acc') and c == p))
        elif _is(c, 'rest'):
            parse(c, 'rest', (_is(p, 'rest') or not dic['rest']))
        elif _is(c, 'app'):
            parse(c, 'app', (dic['note'] and dic['dur']))
        elif _is(c, 'art'):
            dic['art'].append(kern.art[c])
        elif _is(c, 'beam'):
            dic['beam'].append(kern.beams[c])
        elif _is(c, 'acciac'):
            dic['acciac'].append(c)
        else:
            print("Humdrum cacter not recognized: " + c)
    return dic


def parse_kern_item(string, lineno, itemno):
    d = kern_tokenizer(string, lineno)

    if (not d['dur']) and ((not d['acciac']) or (not d['app'])):
        kern_error("Duration can't be NULL.")

    if (d['note'] and d['rest']):
        kern_error("A note can't have a pitch and a rest.")

    if d['note']:
        name = parse_kern_note(d['note'], d['acc'], lineno)
        octave = parse_kern_octave(name, lineno)
        # FIXME
        #dur = calculate_duration(d['durs'], d['dots'])
        dur = d['dur']
        code = music.string_to_code(name, "base40")
        return Note(name, dur, d['art'], d['beam'], octave,
                    code, "base40", "kern")
    elif d['rest']:
        # FIXME
        #dur = calculate_duration(d['durs'], d['dots'])
        dur = d['dur']
        wholeNote = False if d['rest'] or len(d['rest']) >= 1 else True
        return Rest(dur, wholeNote)
    else:
        kern_error("Kern data must have a note or rest.")


def parse_kern(string, linen, itemno):
    s = string.split(" ")

    if not string:
        kern_error("Kern string shoudn't be empty.")
    elif len(s) == 1:
        return parse_kern_item(string, linen, itemno)
    else:
        return MultipleStop([parse_kern_item(i, linen, itemno) for i in s])

## Parse dynam


def parse_dynam(string, lineno, itemno):
    return string

## parse elements


def unknown_type(item, lineno, itemno):
    return item


def parse_bar(string):
    return Bar(utils.isMatch("[0-9]+([a-z]+)?", string),
               utils.isMatch(":\\||:!", string),
               utils.isMatch("\\|:|!:", string),
               utils.isMatch("==", string))


def parse_tandem(string):
    return Tandem(string, None)


def parse_data(item, lineno, itemno, data_type):
    dic = {"kern": parse_kern,
           "dynam": parse_dynam}

    return dic.get(data_type, unknown_type)(item, lineno, itemno)

## basic parser


def parse_spine_item(item, lineno, itemno, score):
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
        data_type = score.spine_types[itemno]
        return parse_data(item, lineno, itemno, data_type)


def parse_reference_record(line):
    s = line.split(":", 1)
    return Record(s[0][3:], s[1])


def parse_global_comment(line):
    return Comment(line)


def parse_spine(line, lineno, score):
    list = []
    itemno = 0
    for item in line.split("\t"):
        list.append(parse_spine_item(item, lineno, itemno, score))
        itemno += 1
    return(list)


def parse_line(line, score, lineno):
    lineno += 1
    if utils.isMatch(r"^[ \t]*$", line) is not None:
        score.append(BlankLine())
    elif utils.isMatch(r"^!{3}[a-zA-Z ]+", line):
        score.append(parse_reference_record(line))
    elif utils.isMatch(r"^(!{2})|(!{4,})[a-zA-Z ]+", line):
        score.append(parse_global_comment(line))
    else:
        score.append(parse_spine(line, lineno, score))
    return score


def parse_string(string):
    lineno = 0
    score = Score()
    for line in string.split('\n'):
        parse_line(line, score, lineno)
    return score


def parse_file(file):
    lineno = 0
    score = Score()
    with open(file) as f:
        for line in f.read().split('\n'):
            parse_line(line, score, lineno)
        return score

## test usage

if __name__ == "__main__":
    #f = parse_file("/home/kroger/Documents/xenophilus/data/k160-02.krn")
    f = parse_file("/home/kroger/Documents/xenophilus/data/test.krn")
    for item in f.data:
        print(item)
