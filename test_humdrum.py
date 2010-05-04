import humdrum as h
import score
from fractions import Fraction as frac
import py


def test_parse_kern_note():
    n1 = h.parse_kern_note('ddd', '##')
    n2 = h.parse_kern_note('ccc', '###')
    n3 = h.parse_kern_note('eee', '--')
    n4 = h.parse_kern_note('e', '')
    assert n1 == "D##"
    assert n2 == "C###"
    assert n3 == "Ebb"
    assert n4 == "E"


def test_parse_kern_octave():
    assert h.parse_kern_octave('EEE', '#') == 1
    assert h.parse_kern_octave('DD', '') == 2
    assert h.parse_kern_octave('CC', '') == 2
    assert h.parse_kern_octave('C', '') == 3
    assert h.parse_kern_octave('c', '') == 4
    assert h.parse_kern_octave('dd', '') == 5
    assert h.parse_kern_octave('eee', '#') == 6
    assert h.parse_kern_octave('eee', '##') == 6
    assert h.parse_kern_octave('eee', '###') == 6
    assert h.parse_kern_octave('FF', '--') == 2
    assert h.parse_kern_octave('GGG', '#') == 1
    # a few boundary cases, where accidentals change the octave
    assert h.parse_kern_octave('c', '-') == 3
    assert h.parse_kern_octave('d', '---') == 3
    assert h.parse_kern_octave('b', '#') == 5
    assert h.parse_kern_octave('C', '-') == 2
    assert h.parse_kern_octave('D', '---') == 2
    assert h.parse_kern_octave('B', '#') == 4
    py.test.raises(AssertionError, h.parse_kern_octave, 'CCCCC', '')
    py.test.raises(h.KernError, h.parse_kern_octave, '', '')


def test_kern_tokenizer():
    tokens = h.kern_tokenizer("4.cc##")
    assert tokens['note'] == ['c', 'c']
    assert tokens['acc'] == ['#', '#']
    assert tokens['dur'] == ['4']
    assert tokens['dot'] == ['.']


def test_parse_kern_item1():
    n = h.parse_kern_item("4c")
    assert n.name == 'C'
    assert n.duration == frac(1, 4)
    assert n.octave == 4
    assert n.code == 3
    assert n.system == "base40"
    assert n.type == "kern"


def test_parse_kern_item2():
    n = h.parse_kern_item("4.CC##T;U(L")
    assert n.name == 'C##'
    assert n.duration == frac(3, 8)
    assert n.octave == 2
    assert n.code == 5
    assert n.system == "base40"
    assert n.type == "kern"
    assert 'trill-wt' in n.articulations
    assert 'fermata' in n.articulations
    assert 'mute' in n.articulations
    assert 'slur-start', n.articulations
    assert 'beam-start', n.beams


def test_parse_kern():
    assert isinstance(h.parse_kern("4c"), score.Note)
    assert isinstance(h.parse_kern("4r"), score.Rest)


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
    item = h.parse_item("=2:||:", score.Score())
    assert isinstance(item, score.Bar)


def test_parse_item_einterp():
    item = h.parse_item("**kern", score.Score())
    assert isinstance(item, score.Exclusive)


def test_parse_item_tandem():
    item = h.parse_item("*ClefF4", score.Score())
    assert isinstance(item, score.Tandem)


def test_parse_item_comment():
    item = h.parse_item("! foo", score.Score())
    assert isinstance(item, score.Comment)


def test_parse_item_null():
    item = h.parse_item(".", score.Score())
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
    f = h.parse_line("!!!com: Pedro Kroger", score.Score())
    assert isinstance(f[0], score.Record)


def test_parse_line2():
    f = h.parse_line("!! Global comment", score.Score())
    assert isinstance(f[0], score.Comment)


def test_parse_line3():
    # FIXME: is this a bug?
    f = h.parse_line("", score.Score())
    assert isinstance(f[0], score.BlankLine)


def test_parse_line4():
    line = "**kern\t**kern"
    f = h.parse_line(line, score.Score())
    assert isinstance(f[0][0], score.Exclusive)
    assert isinstance(f[0][1], score.Exclusive)


def test_parse_line5():
    line = "4c	f"
    s = score.Score()
    py.test.raises(h.KernError, h.parse_line, line, s)


def test_parse_line6():
    s = score.Score()
    h.parse_line("**kern	**kern", s)
    h.parse_line("4c	4d", s)
    assert isinstance(s[0][0], score.Exclusive)
    assert isinstance(s[0][1], score.Exclusive)
    assert isinstance(s[1][0], score.Note)
    assert isinstance(s[1][1], score.Note)


def test_parse_line7():
    s = score.Score()
    h.parse_line("!foo\t!! bar", s)
    assert s[0][0].data == "foo"
    assert s[0][1].data == "bar"
    assert s[0][0].level == 1
    assert s[0][1].level == 2

def test_parse_string():
    """We check if the basics of parse_string are working by
    parsing a string with 3 elements (only one spine) and checking
    the type of each element.
    """

    sco1 = h.parse_string("**kern\t**kern\nc4\tc4\n*-\t*-")
    assert sco1.spine_types == ['kern', 'kern']

    sco2 = h.parse_string("**kern\n4c\n*-")

    assert 3 == len(sco2)
    assert isinstance(sco2[0][0], score.Exclusive)
    assert isinstance(sco2[1][0], score.Note)
    assert isinstance(sco2[2][0], score.Tandem)


def test_parse_file():
    """We check if the basics of parse_file are working by parsing
    a file with 3 elements (only one spine) and checking the type
    of each element.
    """

    data = h.parse_file("data/simple1.krn")

    assert 3 == len(data)
    assert isinstance(data[0][0], score.Exclusive)
    assert isinstance(data[1][0], score.Note)
    assert isinstance(data[2][0], score.Tandem)
