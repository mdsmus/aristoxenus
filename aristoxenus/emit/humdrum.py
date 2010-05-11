from __future__ import print_function
import sys
from aristoxenus.score import (Score, Record, Comment, Tandem, Exclusive, UnknownType,
                   Note, MultipleStop, Bar, Rest, NullToken, BlankLine,
                   SpinePath)
from aristoxenus.utils import multimethod
import aristoxenus.music


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

spine_table_humdrum = {
    "spine-end": '-',
    "spine-add": '+',
    "spine-split": '^',
    "spine-join": 'v',
    "spine-swap": 'x'
    }


class ConvertError(Exception):
    pass


## humdrum
@multimethod(Score)
def show(self):
    result = []
    for item in self:
        if type(item) is list:
            result.append("\t".join([show(x) for x in item]))
        else:
            result.append(show(item))
    return "\n".join(result)


@multimethod(Record)
def show(self):
    return "!!! {0}: {1}".format(self.name, self.data)


@multimethod(Comment)
def show(self):
    return "{0} {1}".format(self.level * "!", self.data)


@multimethod(Tandem)
def show(self):
    return "*{0}{1}".format(self.type, self.data)


@multimethod(Exclusive)
def show(self):
    return "**{0}".format(self.name)


@multimethod(Note)
def show(self):
    name = music.notename_to_humdrum(self.name, self.octave)
    dur = music.frac_to_dur(self.duration)
    return "{1}{0}".format(name, dur)


@multimethod(MultipleStop)
def show(self):
    return " ".join([show(x) for x in self])


@multimethod(list)
def show(self):
    return "\t".join([show(x) for x in self])


@multimethod(Bar)
def show(self):
    return "={0}".format(self.number)


@multimethod(SpinePath)
def show(self):
    return "*{0}".format(spine_table_humdrum[self.type])


@multimethod(Rest)
def show(self):
    dur = music.frac_to_dur(self.duration)
    return "{0}r".format(dur)


@multimethod(BlankLine)
def show(self):
    return "\n"


@multimethod(NullToken)
def show(self):
    return "."


@multimethod(UnknownType)
def show(self):
    return self
