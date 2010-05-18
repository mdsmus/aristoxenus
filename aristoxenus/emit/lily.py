from __future__ import print_function
import sys
from aristoxenus import music
from aristoxenus import utils


class PrintLily(utils.Visitor):
    def visit_Score(self, obj):
        spines = [s for s in self.spine_types if s == "kern"]

        print("""\\header {{
        title = \"{0}\"
        composer = \"{1}\"
        }}
        """.format(obj.title, obj.composer), file=stream)

        print("{\n<<\n", file=stream)
        for spine in reversed(range(0, len(spines))):
            print("\\new Staff {", file=stream)
            print(" ".join([show(i) for i in obj.get_spine_simple(spine)]), file=stream)
            print("}", file=stream)
        print(">>\n}\n", file=stream)

    def visit_Note(self, obj):
        name = music.notename_to_lily(obj.name, obj.octave)
        dur = music.frac_to_dur(obj.duration)
        return "{0}{1}".format(name,  dur)

    def visit_Rest(self, obj):
        dur = music.frac_to_dur(obj.duration)
        return "r{0}".format(dur)

    def visit_MultipleStop(self, obj):
        return " ".join([show(x) for x in obj])

    def visit_Bar(self, obj):
        return "|\n"

    def show(self, obj):
        return ""
