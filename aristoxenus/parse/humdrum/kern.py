from collections import defaultdict
from aristoxenus import utils
from aristoxenus import music
from aristoxenus.score import (Score, Record, Comment, Tandem, Exclusive, UnknownType,
                   Note, MultipleStop, Bar, Rest, NullToken, BlankLine,
                   SpinePath)


class KernError(Exception):
    """Exception class for kern data."""
    pass


def kern_error(message, lineno=""):
    """Helper function to raise parsing errors."""

    raise KernError(message, lineno)


debug = False

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

    Humdrum represents flats as dashes ('-'); we replace them with 'b's:

    >>> parse_kern_note('cc', '--')
    'Cbb'
    """

    return note[0].upper() + utils.replace_flats("".join(accs))


def parse_kern_octave(note, accs, lineno=1):
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
        kern_error("Note can't be empty.", lineno)

    n = music.string_to_code(note[0], "", "base12")
    a = music.accidental(accs)

    return octave + ((n + a) // 12)


def kern_tokenizer(item, linen=1):
    tokens = defaultdict(list)

    def _is(char, type):
        return char in types[type][0]

    def parse(char, key, cond):
        tokens[key].append(char) if cond else kern_error(types[key][0], linen)

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
            if debug:
                print("Humdrum character not recognized: " + c)
    return tokens


def parse_kern_item(item, note_system="base40", lineno=1, itemno=1):
    tokens = kern_tokenizer(item, lineno)

    if (not tokens['dur']) and ((not tokens['acciac']) or (not tokens['app'])):
        kern_error("Duration can't be NULL.", lineno)

    if (tokens['note'] and tokens['rest']):
        kern_error("A note can't have a pitch and a rest.", lineno)

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
        note.octave = parse_kern_octave(notename, acc, lineno)
        note.code = music.string_to_code(notename[0], acc, note_system, note.octave)
        note.system = note_system
        note.type = "kern"
        return note
    elif tokens['rest']:
        wholeNote = not bool(tokens['rest'] or len(tokens['rest']) >= 1)
        return Rest(duration, wholeNote)
    else:
        kern_error("Kern data must have a note or rest.", lineno)


def parse_kern(item, note_system="base40", linen=1, itemno=1):
    s = item.split(" ")

    if not item:
        kern_error("Kern item shouldn't be empty.", linen)
    elif len(s) == 1:
        return parse_kern_item(item, note_system, linen, itemno)
    else:
        return MultipleStop([parse_kern_item(i, note_system, linen, itemno) for i in s])
