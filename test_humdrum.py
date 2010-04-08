import humdrum as h
import score
from fractions import Fraction as frac


def test_parse_kern_note():
    n1 = h.parse_kern_note(['d', 'd', 'd'], ['#', '#'], 1)
    n2 = h.parse_kern_note(['c', 'c', 'c'], ['#', '#', '#'], 1)
    n3 = h.parse_kern_note(['e', 'e', 'e'], ['-', '-'], 1)
    n4 = h.parse_kern_note(['e'], [], 1)
    assert n1 == "d##"
    assert n2 == "c###"
    assert n3 == "ebb"
    assert n4 == "e"


def test_parse_kern_octave():
    assert h.parse_kern_octave("c", 1) == 4
    assert h.parse_kern_octave("dd", 1) == 5
    assert h.parse_kern_octave("eee#", 1) == 6
    assert h.parse_kern_octave("eee##", 1) == 6
    assert h.parse_kern_octave("eee###", 1) == 6
    assert h.parse_kern_octave("E-", 1) == 3
    assert h.parse_kern_octave("FF--", 1) == 2
    assert h.parse_kern_octave("GGG#", 1) == 1


def test_kern_tokenizer():
    tokens = h.kern_tokenizer("4.cc##", 1)
    assert tokens['note'] == ['c', 'c']
    assert tokens['acc'] == ['#', '#']
    assert tokens['dur'] == ['4']
    assert tokens['dot'] == ['.']


def test_parse_kern_item1():
    n = h.parse_kern_item("4c", 1, 1)
    assert n.name == 'c'
    assert n.duration == frac(1, 4)
    assert n.octave == 4
    assert n.code == 3
    assert n.system == "base40"
    assert n.type == "kern"


def test_parse_kern_item2():
    n = h.parse_kern_item("4.CC##T;U(L", 1, 1)
    assert n.name == 'c##'
    assert n.duration == frac(3, 8)
    assert n.octave == 6
    assert n.code == 5
    assert n.system == "base40"
    assert n.type == "kern"
    assert 'trill-wt' in n.articulations
    assert 'fermata' in n.articulations
    assert 'mute' in n.articulations
    assert 'slur-start', n.articulations
    assert 'beam-start', n.beams


def test_parse_kern():
    assert isinstance(h.parse_kern("4c", 1, 1), score.Note)
    assert isinstance(h.parse_kern("4r", 1, 1), score.Rest)


def test_parse_dynam():
    assert isinstance(h.parse_dynam("fff", 1, 1), score.Dynam)


def test_parse_bar():
    bar = h.parse_bar("=2:||:")
    assert bar.number == "2"
    assert bar.repeat_begin == True
    assert bar.repeat_end == True
    assert bar.double == False
    bar2 = h.parse_bar("==2")
    assert bar2.double == True


def test_parse_tandem():
    assert "fixme, please" == h.parse_tandem("*IVox")


def test_parse_item_bar():
    item = h.parse_item("=2:||:", 1, 1, score.Score())
    assert isinstance(item, score.Bar)


def test_parse_item_einterp():
    item = h.parse_item("**kern", 1, 1, score.Score())
    assert isinstance(item, score.Exclusive)


def test_parse_item_tandem():
    item = h.parse_item("*ClefF4", 1, 1, score.Score())
    assert isinstance(item, score.Tandem)


def test_parse_item_comment():
    item = h.parse_item("! foo", 1, 1, score.Score())
    assert isinstance(item, score.Comment)


def test_parse_item_null():
    item = h.parse_item(".", 1, 1, score.Score())
    assert isinstance(item, score.NullToken)


def test_parse_reference_record():
    f = h.parse_reference_record("!!! COM: J. S. Bach")

    assert f.name == 'COM'
    assert f.data == 'J. S. Bach'


def test_parse_comment():
    c1 = h.parse_comment("!! foobar")
    c2 = h.parse_comment("!! foobar!")
    assert c1.data == "foobar"
    assert c2.data == "foobar!"


# parse_line can't parse a single line like '4c f' without context
# because parse_line doesn't know the type of the spines. When
# parse_line parses a line like '**kern' it will store the spine type
# in score.spine_types. At this stage the best we can do is to parse
# reference records, global comments, single lines, and exclusive
# interpretation. If you want to parse things like kern data, you
# should use parse_kern_item instead.


def test_parse_line1():
    f = h.parse_line("!!!com: Pedro Kroger", score.Score(), 1)
    assert isinstance(f.data[0], score.Record)


def test_parse_line2():
    f = h.parse_line("!! Global comment", score.Score(), 1)
    assert isinstance(f.data[0], score.Comment)


def test_parse_line3():
    # FIXME: is this a bug?
    f = h.parse_line("", score.Score(), 1)
    assert isinstance(f.data[0], score.BlankLine)


def test_parse_line4():
    line = "**kern	**kern"
    f = h.parse_line(line, score.Score(), 1)
    assert isinstance(f.data[0], score.Exclusive)
    assert isinstance(f.data[1], score.Exclusive)


def test_parse_line5():
    line = "4c	f"
    s = score.Score()
    try:
        h.parse_line(line, s, 1)
        raise Exception
    except h.KernError:
        pass


def test_parse_line6():
    s = score.Score()
    h.parse_line("**kern	**kern", s, 1)
    h.parse_line("4c	4d", s, 1)
    assert isinstance(s.data[0][0], score.Exclusive)
    assert isinstance(s.data[0][1], score.Exclusive)
    assert isinstance(s.data[1][0], score.Note)
    assert isinstance(s.data[1][1], score.Note)


def test_parse_string():
    """We check if the basics of parse_string are working by
    parsing a string with 3 elements (only one spine) and checking
    the type of each element.
    """

    data = h.parse_string("**kern\n4c\n*-").data

    assert 3 == len(data)
    assert isinstance(data[0][0], score.Exclusive)
    assert isinstance(data[1][0], score.Note)
    assert isinstance(data[2][0], score.Tandem)


def test_parse_file():
    """We check if the basics of parse_file are working by parsing
    a file with 3 elements (only one spine) and checking the type
    of each element.
    """

    data = h.parse_file("data/simple1.krn").data

    assert 3 == len(data)
    assert isinstance(data[0][0], score.Exclusive)
    assert isinstance(data[1][0], score.Note)
    assert isinstance(data[2][0], score.Tandem)
