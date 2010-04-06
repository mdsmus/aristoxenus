class Base(object):
    repr = ''

    def __repr__(self):
        space = ' ' if self.repr else ''
        name = self.__class__.__name__
        return "<{0}{1}{2}>".format(name, space, self.repr)


class Score(Base):
    def append(self, item):
        self.data.append(item)

    def __init__(self):
        self.title = ""
        self.composer = ""
        self.data = []
        self.filename = ""
        self.spine_number = 0
        self.spine_types = []


class Record(Base):
    def __init__(self, name, data):
        self.name = name
        self.data = data


class Comment(Base):
    def __init__(self, data, level=2):
        self.data = data
        self.level = level
        self.repr = data


class Tandem(Base):
    def __init__(self, spine_type, data):
        self.type = spine_type
        self.data = data
        self.repr = spine_type


class ExclusiveInterpretation(Base):
    def __repr__(self):
        return "<**" + self.name + ">"

    def __init__(self, name):
        self.name = name


class Note(Base):
    def __init__(self, name, dur):
        self.name = name
        self.duration = dur
        self.articulations = []
        self.beams = []
        self.octave = 4
        self.code = None
        self.system = None
        self.type = None
        self.repr = "{0}{1}".format(name, dur)


class MultipleStop(list):
    def __repr__(self):
        return '<MS: ' + str(self.__getslice__(0, self.__sizeof__())) + '>'


class Bar(Base):
    def __init__(self, number, repeat_begin=False,
                 repeat_end=False, double=False):
        self.number = number or ""
        self.repeat_begin = repeat_begin
        self.repeat_end = repeat_end
        self.double = double
        self.repr = self.number


class Rest(Base):
    def __init__(self, dur, wholeNote=False):
        self.duration = dur
        self.print_as_whole = wholeNote
        self.repr = "{0}".format(dur)


class NullToken(Base):
    pass


class BlankLine(Base):
    pass
