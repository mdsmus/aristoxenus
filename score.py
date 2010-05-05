import music


class Score(list):
    def __init__(self, *args):
        list.__init__(self, args)
        self.title = ""
        self.composer = ""
        self.filename = ""
        self.spine_types = []


class Record(object):
    def show_as_humdrum(self):
        return "!!! {0}: {1}".format(self.name, self.data)

    def __init__(self, name, data):
        self.name = name
        self.data = data


class Comment(object):
    def show_as_humdrum(self):
        return "{0} {1}".format(self.level * "!", self.data)
        
    def __init__(self, data, level):
        self.data = data
        self.level = level


class Tandem(object):
    def show_as_humdrum(self):
        return "*{0}{1}".format(self.type, self.data)

    def __init__(self, type, data):
        self.type = type
        self.data = data


class Exclusive(object):
    def show_as_humdrum(self):
        return "**{0}".format(self.name)

    def __init__(self, name):
        self.name = name


class Note(object):
    def show_as_humdrum(self):
        name = music.notename_to_humdrum(self.name, self.octave)
        return "{1}{0}".format(name, self.duration ** -1)

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


class Bar(object):
    def show_as_humdrum(self):
        return "={0}".format(self.number)

    def __init__(self, number, repeat_begin=False,
                 repeat_end=False, double=False):
        self.number = number or ""
        self.repeat_begin = repeat_begin
        self.repeat_end = repeat_end
        self.double = double


class Rest(object):
    def show_as_humdrum(self):
        return "{0}r".format(self.duration ** -1)

    def __init__(self, dur, wholenote=False):
        self.duration = dur
        self.print_as_whole = wholenote


class BlankLine(object):
    def show_as_humdrum(self):
        return "\n"


class NullToken(object):
    def show_as_humdrum(self):
        return "."


class Dynam(object):
    def __init__(self, data):
        self.data = data


class UnknownType(str):
    def show_as_humdrum(self):
        return self

    
def make_notes(notes):
    """return a :class:`score.Score` with the notes written as a string."""

    lst = [Note(n) for n in notes.split()]
    return Score(*lst)
