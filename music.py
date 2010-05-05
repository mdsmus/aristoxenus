from __future__ import division
from fractions import Fraction


class MusicError(Exception):
    pass


def calculate_duration(dur, dots=0):
    """Calculate the total duration of a note with augmentation dots.

    :param dur: reciprocal of usual note values (e.g. 8th note has the value of 8)
    :param dots: number of duration dots
   
    The total duration of a note is :math:`\\sum_{i=0} \\frac{R}{2^i}`
    where R is the reciprocal of ``dur``. For instance, a
    note with a duration like '16..' will have a total duration of
    1/16 + 1/32 + 1/64 = 7/64.
    
    >>> calculate_duration(16, 2)
    Fraction(7, 64)
    """

    if dur == 0 or dur == "breve" or dur == "brevis":
        base = Fraction(2, 1)
    elif dur == "longa":
        base = Fraction(4, 1)
    elif dur == "maxima":
        base = Fraction(8, 1)
    elif isinstance(dur, int):
        base = Fraction().from_decimal(dur) ** -1
    else:
        raise MusicError, "I don't recognize duration {0}".format(dur)
    
    return sum([base / (2 ** x) for x in range(0, dots + 1)])


def accidental(acc):
    if acc:
        op = 1 if acc[0] == "#" else -1
    else:
        op = 0

    return len(acc) * op


def string_to_code(notename, acc, code):
    """
    >>> string_to_code('b', '#', 'base12')
    0
    """
    
    notes = "c d e f g a b".split()
    dic = {'base40': ([3, 9, 15, 20, 26, 32, 38], 40),
           'base12': ([0, 2, 4, 5, 7, 8, 11], 12)}

    code_list = dic[code][0]
    n = code_list[notes.index(notename.lower())]
    return  (n + accidental(acc)) % dic[code][1]


def notename_to_humdrum(notename, octave):
    """
    >>> note_to_humdrum('Cbb', 5)
    cc--
    """
    
    note = notename[0]
    acc = notename[1:].replace("b", "-")

    if octave > 3:
        return (note.lower() * (octave - 3)) + acc
    else:
        return (note.upper() * (4 - octave)) + acc


def notename_to_lily(notename, octave):
    """
    >>> note_to_lily('Cb', 5)
    cb''
    """

    note = notename[0]
    acc = notename[1:].replace("b", "es").replace("#", "is")

    if octave > 3:
        print (octave - 3)
        o = "'" * (octave - 3)
    else:
        o = "," * (3 - octave)

    return note.lower() + acc + o
