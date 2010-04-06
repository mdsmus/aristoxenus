from __future__ import print_function
from __future__ import division
from collections import defaultdict
from fractions import Fraction
from itertools import izip, count
import re
from score import (Score, Record, Comment, Tandem, Exclusive,
                   Note, MultipleStop, Bar, Rest, NullToken, BlankLine)
import utils
import music

# FIXME: write documentation
"""
blablag
"""


class KernError(Exception):
    pass


def kern_error(message):
    raise KernError(message)


## Parse kern

art = {'n': "natural",
       '/': "up-stem",
       '\\': "down-stem",
       'o': "harmonic",
       't': "trill-st",
       'T': "trill-wt",
       'S': "turn",
       '$': "inverted-turn",
       'R': "end-with-turn",
       'u': "down-bow",
       'H': "glissando-start",
       'h': "glissando-end",
       ';': "fermata",
       'Q': "gruppetto",
       'p': "app-main-note",
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
       'v': "up-bow",
       'z': "sforzando",
       ',': "breath",
       'm': "mordent-st",
       'w': "inverted-mordent-st",
       'M': "mordent-wt",
       'W': "inverted-mordent-wt"}

beams = {'L': 'beam-start',
         'J': 'beam-end',
         'K': 'beam-partial-right',
         'k': 'beam-partial-left'}


types = {'dur': ("0123456789", "Duration must be together."),
         'note': ("abcdefgABCDEFG", "Notes must be together."),
         'dot': (".", "Dots must be together or after a number."),
         'acc': ("#-", "Accs."),
         'art': (art,),
         'beam': (beams,),
         'rest': ("r", "Rest."),
         'acciac': ("q", "App"),
         'app': ("P",)}


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
    """pylint R0912 """
    tokens = defaultdict(list)

    def _is(char, type):
        return char in types[type][0]

    def parse(char, key, cond):
        tokens[key].append(char) if cond else kern_error(types[key][0])

    for i in range(0, len(token)):
        p = '' if i == 0 else token[i - 1]
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
            tokens['art'].append(art[c])
        elif _is(c, 'beam'):
            tokens['beam'].append(beams[c])
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
    return Bar(utils.search_string("[0-9]+([a-z]+)?", item),
               bool(utils.search_string(":\\||:!", item)),
               bool(utils.search_string("\\|:|!:", item)),
               bool(utils.search_string("==", item)))


def parse_tandem(item):
    # FIXME: implement
    return Tandem(item, None)


def parse_data(item, lineno, itemno, data_type):
    types = {"kern": parse_kern,
             "dynam": parse_dynam}

    return types.get(data_type, unknown_type)(item, lineno, itemno)


## basic parser


def parse_item(item, lineno, itemno, score):
    """
    """

    if item.startswith("="):
        return parse_bar(item)
    elif item.startswith("**"):
        spine_type = item[2:]
        score.spine_types.append(spine_type)
        return Exclusive(spine_type)
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
    """Separate the data in the Reference from the ! character.

    Since a reference record must start with 3 exclamantion marks we
    don't need to use regular expressions to separate the actual
    comment from the comment character. We split the line by the first
    occurency of":" in order to prevent splitting a colon inside the text,
    such as '!!!OTL: Title: more stuff'
    """

    s = line.split(":", 1)
    return Record(s[0][3:].strip(), s[1].strip())


def parse_comment(line):
    """Separate the actual comment from the comment character."""

    match = re.match("^(!+)(.*)$", line)
    return Comment(match.group(2).strip(), len(match.group(1)))


def parse_line(line, score, lineno):
    """Parse a line and append the parsed line into the score.

    A line can be a BlankLine, a reference record, a comment, or have
    tabular data (spines) in which case we parse each item
    individually. Both reference record and comments start with !, but
    a reference record starts with 3 exclamation marks (!!!) while a
    comment starts with one, two, four or more exclamation marks.
    Global comments have more than one exclamation marks and will be
    catched by this function. Local comments have only one exclamation
    mark and are aplied to an individual spine. A local comment will
    be catched in parse_item().
    """

    if utils.search_string(r"^[ \t]*$", line) is not None:
        score.append(BlankLine())
    elif utils.search_string(r"^!{3}[a-zA-Z ]+", line):
        score.append(parse_reference_record(line))
    elif utils.search_string(r"^(!{2})|(!{4,})[a-zA-Z ]+", line):
        score.append(parse_comment(line))
    else:
        s = line.split("\t")
        parsed = [parse_item(i, lineno, n, score) for i, n in izip(s, count())]
        score.append(parsed)
    return score


def parse_string(string):
    """Helper function to parse small strings containing humdrum code.

    This function is useful mainly for tests and to parse data
    directly from user input. To parse large quantities of data you
    should use parse_file() instead.
    """

    score = Score()
    for line, lineno in izip(string.split('\n'), count(1)):
        parse_line(line, score, lineno)
    return score


def parse_file(name):
    """Parse a humdrum file and return an object of type Score."""

    # We don't use parse_string because it's probably faster (and save
    # memory) to iterate the file one line at time using for.
    with open(name) as f:
        score = Score()
        for line, lineno in izip(f, count(1)):
            parse_line(line.rstrip(), score, lineno)
        return score


if __name__ == "__main__":
    #f = parse_file("data/k160-02.krn")
    f = parse_file("data/test.krn")
    #print(f.data)
    for item in f.data:
        print(item)
