from __future__ import print_function
from __future__ import division
from collections import defaultdict
from itertools import izip, count
import re
from score import (Score, Record, Comment, Tandem, Exclusive,
                   Note, MultipleStop, Bar, Rest, NullToken, BlankLine)
import utils
import music


class KernError(Exception):
    """Exception class for kern data."""
    pass


def kern_error(message):
    """Helper function to raise parsing errors."""

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


def parse_kern_note(note, accs):
    """Return a string representation of a note from the tokenizer representation.

    Humdrum represents flats as dashs ('-'); we replace them with 'b's:
    
    >>> parse_kern_note('cc', '--')
    'Cbb'
    """

    return note[0].upper() + "".join(accs).replace("-", "b")


def parse_kern_octave(note, accs):
    """Calculate the octave of a note in the kern representation.

    Since kern uses repetition and case to indicate octave, we need to
    parse it. The central octave is 4, these are the most common
    octaves: ccc = 6, cc = 5, c = 4, C = 3, CC = 2, CCC = 1, CCCC = 0

    This is a basic example of use:
    
    >>> parse_kern_octave('bb', '')
    5

    And we need to take care of the cases where an accidental will
    change the octave:
    
    >>> parse_kern_octave('bb', '#')
    6
    """
    
    size = len(note)

    if size > 0:
        if note[0].islower():
            octave = 3 + size
        else:
            octave = -size + 4
            assert size <= 4, "octave can't be lower than 0, the value is " + str(octave)
    else:
        kern_error("Note can't be empty.")

    n = music.string_to_code(note[0], "", "base12")
    a = music.accidental(accs)

    return octave + ((n + a) // 12)


def kern_tokenizer(item, linen=1):
    tokens = defaultdict(list)

    def _is(char, type):
        return char in types[type][0]

    def parse(char, key, cond):
        tokens[key].append(char) if cond else kern_error(types[key][0])

    for i in range(0, len(item)):
        p = '' if i == 0 else item[i - 1]
        c = item[i]

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


def parse_kern_item(item, lineno=1, itemno=1):
    tokens = kern_tokenizer(item, lineno)

    if (not tokens['dur']) and ((not tokens['acciac']) or (not tokens['app'])):
        kern_error("Duration can't be NULL.")

    if (tokens['note'] and tokens['rest']):
        kern_error("A note can't have a pitch and a rest.")

    dur = int("".join(tokens['dur']))
    dots = len(tokens['dot'])
    duration = music.calculate_duration(dur, dots)
    
    if tokens['note']:
        notename = "".join(tokens['note'])
        acc = "".join(tokens['acc'])
        name = parse_kern_note(notename, acc)
        note = Note(name, duration)
        note.articulations = tokens['art']
        note.beams = tokens['beam']
        note.octave = parse_kern_octave(notename, acc)
        note.code = music.string_to_code(notename[0], acc, "base40")
        note.system = "base40"
        note.type = "kern"
        return note
    elif tokens['rest']:
        wholeNote = not bool(tokens['rest'] or len(tokens['rest']) >= 1)
        return Rest(duration, wholeNote)
    else:
        kern_error("Kern data must have a note or rest.")


def parse_kern(item, linen=1, itemno=1):
    s = item.split(" ")

    if not item:
        kern_error("Kern item shoudn't be empty.")
    elif len(s) == 1:
        return parse_kern_item(item, linen, itemno)
    else:
        return MultipleStop([parse_kern_item(i, linen, itemno) for i in s])


## parse elements


def parse_bar(item):
    """Search a string for bar elements and return a :class:`score.Bar`

    This function will search for the bar number, if a bar begins or
    ends a repetition and if it's a double bar. Humdrum has a bunch of
    syntax for visual barlines that we don't parse. See :ref:`todo`.
    """
    
    return Bar(utils.search_string("[0-9]+([a-z]+)?", item),
               bool(utils.search_string(":\\||:!", item)),
               bool(utils.search_string("\\|:|!:", item)),
               bool(utils.search_string("==", item)))


def parse_tandem(item):
    """FIXME: implement"""
    return Tandem(item, None)


def parse_data(data_type, item, lineno=1, itemno=1):
    """Apply the right function to parse ``data_type``.

    For instance, if ``data_type`` is 'kern', then ``parse_data`` will
    apply ``parse_kern`` to the rest of arguments. ``parse_data`` has
    a dispatch table to match the data type to the function. When the
    parser for a new humdrum data type is implemented, the dispatch
    table need to be updated. If an unknown type is found the item
    will be returned without any parsing.
    """

    def unknown_type(item, lineno=1, itemno=1):
        return UnknownType(item)

    dispatch = {"kern": parse_kern}

    return dispatch.get(data_type, unknown_type)(item, lineno, itemno)


## basic parser


def parse_item(item, score, lineno=1, itemno=1):
    """Parse each item of a humdrum spine.

    We can parse general items like :class:`score.Bar`,
    :class:`score.Exclusive`, :class:`score.Tandem`,
    :class:`score.Comment`, and :class:`score.NullToken` without
    previous information since the type of data is defined in the
    string itself (e.g. the '**' in '**kern' defines it as an
    exclusive interpretation). However, we can't parse other data
    records without knowing their spine type. When an exclusive
    interpretation is found the spine type is appended to
    :attr:`Score.spine_types`. This attribute can be used to know the
    spine type of an item.
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
        return parse_comment(item)
    elif item == ".":
        return NullToken()
    else:
        spine_type_list = score.spine_types
        if len(spine_type_list) == 0:
            kern_error("Can't parse an item without knowing the spine type.")
        else:
            data_type = score.spine_types[itemno]
        return parse_data(data_type, item, lineno, itemno)


def parse_reference_record(line):
    """Separate the data in the Reference from the ! character.

    Since a reference record must start with 3 exclamantion marks we
    don't need to use regular expressions to separate the actual
    comment from the comment character. We split the line by the first
    occurency of ':' in order to prevent splitting a colon inside the
    text, such as '!!!OTL: Title: more stuff'.
    """

    s = line.split(":", 1)
    return Record(s[0][3:].strip(), s[1].strip())


def parse_comment(line):
    """Separate the actual comment from the comment character."""

    match = re.match("^(!+)(.*)$", line)
    return Comment(match.group(2).strip(), len(match.group(1)))


def parse_line(line, score, lineno=1):
    """Parse a line, append the parsed result into the score and return the score

    A line can be a BlankLine, a reference record, a comment, or have
    tabular data (spines) in which case we parse each item
    individually with :func:`humdrum.parse_item`. Both reference
    record and comments start with !, but a reference record starts
    with 3 exclamation marks (!!!) while a comment starts with one,
    two, four or more exclamation marks. Global comments have more
    than one exclamation marks and will be catched by this function.
    Local comments have only one exclamation mark and are aplied to an
    individual spine. A local comment will be catched in
    :func:`humdrum.parse_item()`.
    """

    if utils.search_string(r"^[ \t]*$", line) is not None:
        score.append(BlankLine())
    elif utils.search_string(r"^!{3}[a-zA-Z ]+", line):
        score.append(parse_reference_record(line))
    elif utils.search_string(r"^(!{2})|(!{4,})[a-zA-Z ]+", line):
        score.append(parse_comment(line))
    else:
        s = line.split("\t")
        parsed = [parse_item(i, score, lineno, n) for i, n in izip(s, count())]
        score.append(parsed)
    return score


def parse_string(string):
    """Parse a string with humdrum data  and return a :class:`score.Score`.

    This function is useful mainly for tests and to parse data
    directly from user input. To parse large quantities of data you
    should use :func:`parse_file()` instead.
    """

    s = Score()
    for line, lineno in izip(string.split('\n'), count(1)):
        parse_line(line, s, lineno)
    return s


def parse_file(filename):
    """Parse a humdrum file and return a :class:`score.Score`."""

    with open(filename) as f:
        s = Score()
        for line, lineno in izip(f, count(1)):
            parse_line(line.rstrip(), s, lineno)
        return s


if __name__ == "__main__":
    #f = parse_file("data/k160-02.krn")
    f = parse_file("data/test.krn")
