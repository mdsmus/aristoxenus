from __future__ import print_function
from score import (Score, Record, Comment, Tandem, Exclusive, UnknownType,
                   Note, MultipleStop, Bar, Rest, NullToken, BlankLine)
from multimethod import multimethod


humdrum_table = {
    'natural': "n",
    "up-stem": '/',
    "down-stem": '\\',
    "harmonic": 'o',
    "trill-st": 't',
    "trill-wt": 'T',
    "turn": 'S',
    "inverted-turn": '$',
    "end-with-turn": 'R',
    "down-bow": 'u',
    "glissando-start": 'H',
    "glissando-end": 'h',
    "fermata": ';',
    "gruppetto": 'Q',
    "app-main-note": 'p',
    "mute": 'U',
    "tie-start": '[',
    "tie-end": ']',
    "tie-midle": '_',
    "slur-start": '(',
    "slur-end": ')',
    "phrase-start": '{',
    "phrase-end": '}',
    "staccato": '\'',
    "spiccato": 's',
    "pizzicato": '\\',
    "staccatissimo": '`',
    "tenuto": '~',
    "accent": '^',
    "arpeggiation": ':',
    "up-bow": 'v',
    "sforzando": 'z',
    "breath": ',',
    "mordent-st": 'm',
    "inverted-mordent-st": 'w',
    "mordent-wt": 'M',
    "inverted-mordent-wt": 'W',
    'beam-start': 'L',
    'beam-end': 'J',
    'beam-partial-right': 'K',
    'beam-partial-left': 'k'
    }


class ConvertError(Exception):
    pass


## humdrum
@multimethod(Score)
def show_as_humdrum(self):
    for item in self:
        if type(item) is list:
            print("\t".join([show_as_humdrum(x) for x in item]))
        else:
            print(show_as_humdrum(item))


@multimethod(Record)
def show_as_humdrum(self):
    return "!!! {0}: {1}".format(self.name, self.data)


@multimethod(Comment)
def show_as_humdrum(self):
    return "{0} {1}".format(self.level * "!", self.data)


@multimethod(Tandem)
def show_as_humdrum(self):
    return "*{0}{1}".format(self.type, self.data)


@multimethod(Exclusive)
def show_as_humdrum(self):
    return "**{0}".format(self.name)


@multimethod(Note)
def show_as_humdrum(self):
    name = music.notename_to_humdrum(self.name, self.octave)
    return "{1}{0}".format(name, self.duration ** -1)


@multimethod(MultipleStop)
def show_as_humdrum(self):
    return " ".join([show_as_humdrum(x) for x in self])


@multimethod(Bar)
def show_as_humdrum(self):
    return "={0}".format(self.number)


@multimethod(Rest)
def show_as_humdrum(self):
    return "{0}r".format(self.duration ** -1)


@multimethod(BlankLine)
def show_as_humdrum(self):
    return "\n"


@multimethod(NullToken)
def show_as_humdrum(self):
    return "."


@multimethod(UnknownType)
def show_as_humdrum(self):
    return self


## lily

@multimethod(Score)
def show_as_lily(self):
    spines = [s for s in self.spine_types if s == "kern"]
    print("{\n<<\n")
    for spine in range(0, len(spines)):
        print("\\new Staff {")
        print(" ".join([show_as_lily(i) for i in self.get_spine_simple(spine)]))
        print("}")
    print(">>\n}\n")


@multimethod(Record)
def show_as_lily(self):
    return ""


@multimethod(Comment)
def show_as_lily(self):
    return ""


@multimethod(Tandem)
def show_as_lily(self):
    return ""


@multimethod(Exclusive)
def show_as_lily(self):
    return ""


@multimethod(Note)
def show_as_lily(self):
    name = music.notename_to_lily(self.name, self.octave)
    return "{0}{1}".format(name, self.duration ** -1)


@multimethod(MultipleStop)
def show_as_lily(self):
    return " ".join([show_as_lily(x) for x in self])


@multimethod(Bar)
def show_as_lily(self):
    return "|"


@multimethod(Rest)
def show_as_lily(self):
    return "r{0}".format(self.duration ** -1)


@multimethod(BlankLine)
def show_as_lily(self):
    return ""


@multimethod(NullToken)
def show_as_lily(self):
    return ""


@multimethod(UnknownType)
def show_as_lily(self):
    return ""
