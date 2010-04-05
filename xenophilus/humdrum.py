from __future__ import print_function
from __future__ import division
from collections import defaultdict
from fractions import Fraction
import math
import operator
import sys
from itertools import izip, count

if __name__ == "__main__":
    import utils
    import music
    import kern
else:
    from . import utils
    from . import music
    from . import kern

## classes definitions


class Base(object):
    __repr = ''

    def __repr__(self):
        space = ' ' if self.__repr else ''
        name = self.__class__.__name__
        return "<{0}{1}{2}>".format(name, space, self.__repr)


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
    def __init__(self, data, level=2):
        self.data = data
        self.level = level


class Tandem(Base):
    def __init__(self, spine_type, data):
        self.type = spine_type
        self.data = data
        self.__repr = spine_type


class ExclusiveInterpretation(Base):
    def __repr__(self):
        return "<**" + self.name + ">"

    def __init__(self, name):
        self.name = name


class Note(Base):
    def __init__(self, name, dur):
        self.name = name
        self.duration = dur
        self.articulations = []
        self.beams = []
        self.octave = 4
        self.code = None
        self.system = None
        self.type = None
        self.__repr = "{0}{1}".format(name, dur)


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
        self.__repr = self.number


class Rest(Base):
    def __init__(self, dur, wholeNote=False):
        self.duration = dur
        self.print_as_whole = wholeNote
        self.__repr = "{0}".format(dur)


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
    assert isinstance(note, list) and isinstance(accs, list)
    return note[0].lower() + "".join(accs).replace("-", "b")


def parse_kern_octave(note, lineno):
    # FIXME: nasty bug with accidentals (see tests)
    if note[0].islower:
        return 3 + len(note)
    else:
        value = [3, 2, 1, 0][note[-1]]
        return value or kern_error("Octave is too low.")


def kern_tokenizer(token, linen):
    tokens = defaultdict(list)

    def _is(char, type):
        return char in kern.types[type][0]

    def parse(char, key, cond):
        tokens[key].append(char) if cond else kern_error(kern.types[key][0])

    for i in range(0, len(token)):
        p = utils.prev_string(token, i)
        c = token[i]

        if _is(c, 'dur'):
            parse(c, 'dur', (not p or not tokens['dur'] or _is(p, 'dur')))
        elif _is(c, 'note'):
            parse(c, 'note', (not p or not tokens['note'] or _is(p, 'note')))
        elif _is(c, 'dot'):
            parse(c, 'dot', (_is(p, 'dur') or _is(p, 'dot')))
        elif _is(c, 'acc'):
            parse(c, 'acc', _is(p, 'note') or (_is(p, 'acc') and c == p))
        elif _is(c, 'rest'):
            parse(c, 'rest', (_is(p, 'rest') or not tokens['rest']))
        elif _is(c, 'app'):
            parse(c, 'app', (tokens['note'] and tokens['dur']))
        elif _is(c, 'art'):
            tokens['art'].append(kern.art[c])
        elif _is(c, 'beam'):
            tokens['beam'].append(kern.beams[c])
        elif _is(c, 'acciac'):
            tokens['acciac'].append(c)
        else:
            print("Humdrum cacter not recognized: " + c)
    return tokens


def parse_kern_item(item, lineno, itemno):
    tokens = kern_tokenizer(item, lineno)

    if (not tokens['dur']) and ((not tokens['acciac']) or (not tokens['app'])):
        kern_error("Duration can't be NULL.")

    if (tokens['note'] and tokens['rest']):
        kern_error("A note can't have a pitch and a rest.")

    if tokens['note']:
        name = parse_kern_note(tokens['note'], tokens['acc'], lineno)
        # FIXME
        #dur = calculate_duration(tokens['durs'], tokens['dots'])
        note = Note(name, tokens['dur'])
        note.articulations = tokens['art']
        note.beams = tokens['beam']
        note.octave = parse_kern_octave(name, lineno)
        note.code = music.string_to_code(name, "base40")
        note.system = "base40"
        note.type = "kern"
        return note
    elif tokens['rest']:
        # FIXME
        #dur = calculate_duration(tokens['durs'], tokens['dots'])
        dur = tokens['dur']
        wholeNote = not bool(tokens['rest'] or len(tokens['rest']) >= 1)
        return Rest(dur, wholeNote)
    else:
        kern_error("Kern data must have a note or rest.")


def parse_kern(item, linen, itemno):
    s = item.split(" ")

    if not item:
        kern_error("Kern item shoudn't be empty.")
    elif len(s) == 1:
        return parse_kern_item(item, linen, itemno)
    else:
        return MultipleStop([parse_kern_item(i, linen, itemno) for i in s])

## Parse dynam


def parse_dynam(item, lineno, itemno):
    # FIXME: implement
    return item

## parse elements


def unknown_type(item, lineno, itemno):
    return item


def parse_bar(item):
    return Bar(utils.isMatch("[0-9]+([a-z]+)?", item),
               bool(utils.isMatch(":\\||:!", item)),
               bool(utils.isMatch("\\|:|!:", item)),
               bool(utils.isMatch("==", item)))


def parse_tandem(item):
    # FIXME: implement
    return Tandem(item, None)


def parse_data(item, lineno, itemno, data_type):
    types = {"kern": parse_kern,
             "dynam": parse_dynam}

    return types.get(data_type, unknown_type)(item, lineno, itemno)


## basic parser


def parse_item(item, lineno, itemno, score):
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
        spine_type_list = score.spine_types
        if len(spine_type_list) == 0:
            kern_error("Can't parse an item without knowing the spine type.")
        else:
            data_type = score.spine_types[itemno]
        return parse_data(item, lineno, itemno, data_type)


def parse_reference_record(line):
    assert line.startswith('!!!'), "A reference record must start with !!!"
    assert ":" in line
    s = line.split(":", 1)
    return Record(s[0][3:].strip(), s[1].strip())


def parse_comment(line):
    assert line.startswith('!'), "A comment must start with a bang !"
    level = line.count('!')
    return Comment(line.strip('!').strip(), level)


def parse_line(line, score, lineno):
    if utils.isMatch(r"^[ \t]*$", line) is not None:
        score.append(BlankLine())
    elif utils.isMatch(r"^!{3}[a-zA-Z ]+", line):
        score.append(parse_reference_record(line))
    elif utils.isMatch(r"^(!{2})|(!{4,})[a-zA-Z ]+", line):
        score.append(parse_comment(line))
    else:
        s = line.split("\t")
        parsed = [parse_item(i, lineno, n, score) for i, n in izip(s, count())]
        score.append(parsed)
    return score


def parse_string(string):
    assert type(string) is str, "argument must be a string, it was " + string

    score = Score()
    for line, lineno in izip(string.split('\n'), count(1)):
        parse_line(line, score, lineno)
    return score


def parse_file(name):
    with open(name) as f:
        return parse_string(f.read())


if __name__ == "__main__":
    #f = parse_file("/home/kroger/Documents/xenophilus/data/k160-02.krn")
    f = parse_file("/home/kroger/Documents/xenophilus/data/test.krn")
    #print(f.data)
    for item in f.data:
        print(item)
