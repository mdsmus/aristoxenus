from __future__ import print_function
import sys
from aristoxenus import music
from aristoxenus import utils

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


class PrintHumdrum(utils.Visitor):
    def visit_Score(self, obj):
        result = []
        for item in obj:
            if type(item) is list:
                result.append("\t".join([show(x) for x in item]))
            else:
                result.append(show(item))
        return "\n".join(result)

    def visit_Record(self, obj):
        return "!!! {0}: {1}".format(obj.name, obj.data)

    def visit_Comment(self, obj):
        return "{0} {1}".format(obj.level * "!", obj.data)

    def visit_Tandem(self, obj):
        data = clefs[obj.data] if obj.type == "clef" else obj.data
        obj_type = tandem.get(obj.type, data)
        return "*{0}{1}".format(obj_type, data)

    def visit_Exclusive(self, obj):
        return "**{0}".format(obj.name)

    def visit_Note(self, obj):
        name = music.notename_to_humdrum(obj.name, obj.octave)
        dur = music.frac_to_dur(obj.duration)
        articulations = [humdrum_table[a] for a in obj.articulations]
        return "{0}{1}{2}".format(dur, name, "".join(articulations))

    def visit_MultipleStop(self, obj):
        return " ".join([show(x) for x in obj])

    def visit_list(self, obj):
        return "\t".join([show(x) for x in obj])

    def visit_Bar(self, obj):
        n = 2 if obj.double else 1
        return "=" * n + str(obj.number)

    def visit_SpinePath(self, obj):
        return "*{0}".format(spine_table_humdrum[obj.type])

    def visit_Rest(self, obj):
        dur = music.frac_to_dur(obj.duration)
        return "{0}r".format(dur)

    def visit_BlankLine(self, obj):
        return "\n"

    def visit_NullToken(self, obj):
        return "."

    def visit_NullInterpretation(self, obj):
        return "*"

    def visit_UnknownType(self, obj):
        return obj


def show(obj):
    p = PrintHumdrum()
    return p.dispatch(obj)
