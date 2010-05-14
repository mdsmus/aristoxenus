from __future__ import print_function
import sys
from aristoxenus.score import *
from aristoxenus.utils import multimethod
from aristoxenus import music


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


clefs = {"bass": "F4",
         "treble": "G2",
         "alto": "C3",
         "tenor": "C4",
         "tenor8": "Gv2",
         "soprano": "C1",
         "mezzo": "C2",
         "perc" : "X"
         }

tandem = {'clef': "clef",
          'instr-class': "IC",
          'instr-group': "IG",
          'transposing': "ITr",
          'instrument': "I",
          'instrument-user': "I:",
          'key-signature': "k",
          'tempo': "MM",
          'meter': "M",
          'timebase': "tb",
          'expansion-list': ">[",
          'label': ">",
          'key': '???'
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
    data = clefs[self.data] if self.type == "clef" else self.data
    return "*{0}{1}".format(tandem[self.type], data)


@multimethod(Exclusive)
def show(self):
    return "**{0}".format(self.name)


@multimethod(Note)
def show(self):
    name = music.notename_to_humdrum(self.name, self.octave)
    dur = music.frac_to_dur(self.duration)
    articulations = [humdrum_table[a] for a in self.articulations]
    return "{0}{1}{2}".format(dur, name, "".join(articulations))


@multimethod(MultipleStop)
def show(self):
    return " ".join([show(x) for x in self])


@multimethod(list)
def show(self):
    return "\t".join([show(x) for x in self])


@multimethod(Bar)
def show(self):
    n = 2 if self.double else 1
    return "=" * n + str(self.number)


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


@multimethod(NullInterpretation)
def show(self):
    return "*"


@multimethod(UnknownType)
def show(self):
    return self
