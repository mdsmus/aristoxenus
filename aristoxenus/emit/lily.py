from __future__ import print_function
import sys
from aristoxenus.score import (Score, Record, Comment, Tandem, Exclusive, UnknownType,
                   Note, MultipleStop, Bar, Rest, NullToken, BlankLine,
                   SpinePath)
from aristoxenus.utils import multimethod
from aristoxenus import music


@multimethod(Score)
def show(self, stream=sys.stdout):
    spines = [s for s in self.spine_types if s == "kern"]

    print("""\\header {{
    title = \"{0}\"
    composer = \"{1}\"
    }}
    """.format(self.title, self.composer), file=stream)

    print("{\n<<\n", file=stream)
    for spine in reversed(range(0, len(spines))):
        print("\\new Staff {", file=stream)
        print(" ".join([show(i) for i in self.get_spine_simple(spine)]), file=stream)
        print("}", file=stream)
    print(">>\n}\n", file=stream)


@multimethod(Note)
def show(self):
    name = music.notename_to_lily(self.name, self.octave)
    dur = music.frac_to_dur(self.duration)
    return "{0}{1}".format(name,  dur)


@multimethod(Rest)
def show(self):
    dur = music.frac_to_dur(self.duration)
    return "r{0}".format(dur)


@multimethod(MultipleStop)
def show(self):
    return " ".join([show(x) for x in self])


@multimethod(Bar)
def show(self):
    return "|\n"


@multimethod()
def show(self):
    return ""
