import music


class Score(list):
    def show_as_humdrum(self):
        for item in self:
            if type(item) is list:
                print("\t".join([x.show_as_humdrum() for x in item]))
            else:
                print(item.show_as_humdrum())

    def show_as_lily(self):
        for spine in range(0, len(self.spine_types)):
            print("\\new Staff {")
            print(" ".join([i.show_as_lily() for i in self.get_spine_simple(spine)]))
            print("}")
            
    def get_spine(self, n):
        tmp = []
        for item in self:
            if type(item) is list:
                tmp.append(item[n])
            else:
                tmp.append(item)
        return tmp

    def get_spine_simple(self, n):
        return [x[n] for x in self if type(x) is list]

    def __init__(self, *args):
        list.__init__(self, args)
        self.title = ""
        self.composer = ""
        self.filename = ""
        self.spine_types = []


class Record(object):
    def show_as_humdrum(self):
        return "!!! {0}: {1}".format(self.name, self.data)

    def show_as_lily(self):
        return ""
    
    def __init__(self, name, data):
        self.name = name
        self.data = data


class Comment(object):
    def show_as_humdrum(self):
        return "{0} {1}".format(self.level * "!", self.data)

    def show_as_lily(self):
        return ""
    
    def __init__(self, data, level):
        self.data = data
        self.level = level


class Tandem(object):
    def show_as_humdrum(self):
        return "*{0}{1}".format(self.type, self.data)

    def show_as_lily(self):
        return ""
    
    def __init__(self, type, data):
        self.type = type
        self.data = data


class Exclusive(object):
    def show_as_humdrum(self):
        return "**{0}".format(self.name)

    def show_as_lily(self):
        return ""
    
    def __init__(self, name):
        self.name = name


class Note(object):
    def show_as_humdrum(self):
        name = music.notename_to_humdrum(self.name, self.octave)
        return "{1}{0}".format(name, self.duration ** -1)

    def show_as_lily(self):
        name = music.notename_to_lily(self.name, self.octave)
        return "{0}{1}".format(name, self.duration ** -1)

    def __init__(self, name, dur=None):
        self.name = name
        self.duration = dur
        self.articulations = []
        self.beams = []
        self.octave = 4
        self.code = None
        self.system = None
        self.type = None


class MultipleStop(list):
    def show_as_humdrum(self):
        return " ".join([x.show_as_humdrum() for x in self])

    def show_as_lily(self):
        return " ".join([x.show_as_lily() for x in self])


class Bar(object):
    def show_as_humdrum(self):
        return "={0}".format(self.number)

    def show_as_lily(self):
        return "|"

    def __init__(self, number, repeat_begin=False,
                 repeat_end=False, double=False):
        self.number = number or ""
        self.repeat_begin = repeat_begin
        self.repeat_end = repeat_end
        self.double = double


class Rest(object):
    def show_as_humdrum(self):
        return "{0}r".format(self.duration ** -1)

    def show_as_lily(self):
        return "r{0}".format(self.duration ** -1)

    def __init__(self, dur, wholenote=False):
        self.duration = dur
        self.print_as_whole = wholenote


class BlankLine(object):
    def show_as_humdrum(self):
        return "\n"

    def show_as_lily(self):
        return ""


class NullToken(object):
    def show_as_humdrum(self):
        return "."

    def show_as_lily(self):
        return ""


class Dynam(object):
    def __init__(self, data):
        self.data = data


class UnknownType(str):
    def show_as_humdrum(self):
        return self

    def show_as_lily(self):
        return ""

    
def make_notes(notes):
    """return a :class:`score.Score` with the notes written as a string."""

    lst = [Note(n) for n in notes.split()]
    return Score(*lst)
