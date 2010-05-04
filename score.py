class Score(list):
    def __init__(self, *args):
        list.__init__(self, args)
        self.title = ""
        self.composer = ""
        self.filename = ""
        self.spine_types = []


class Record(object):
    def __init__(self, name, data):
        self.name = name
        self.data = data


class Comment(object):
    def __init__(self, data, level):
        self.data = data
        self.level = level


class Tandem(object):
    def __init__(self, type, data):
        self.type = type
        self.data = data


class Exclusive(object):
    def __init__(self, name):
        self.name = name


class Note(object):
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
    pass


class Bar(object):
    def __init__(self, number, repeat_begin=False,
                 repeat_end=False, double=False):
        self.number = number or ""
        self.repeat_begin = repeat_begin
        self.repeat_end = repeat_end
        self.double = double


class Rest(object):
    def __init__(self, dur, wholenote=False):
        self.duration = dur
        self.print_as_whole = wholenote


class NullToken(object):
    pass


class BlankLine(object):
    pass


class Dynam(object):
    def __init__(self, data):
        self.data = data


def make_notes(notes):
    """return a :class:`score.Score` with the notes written as a string."""

    lst = [Note(n) for n in notes.split()]
    return Score(*lst)
