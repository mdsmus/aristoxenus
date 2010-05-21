from __future__ import print_function
from aristoxenus.parse.humdrum import main
from aristoxenus import score
import py
import tempfile

# parse_bar

def pytest_funcarg__bar1(request):
    return main.parse_bar("=2:||:")

def pytest_funcarg__bar2(request):
    return main.parse_bar("==2")


def test_parse_bar_number(bar1):
    assert bar1.number == "2"

def test_parse_bar_repeat_begin(bar1):
    assert bar1.repeat_begin == True

def test_parse_bar_repeat_end(bar1):
    assert bar1.repeat_end == True

def test_parse_bar_double(bar1):
    assert bar1.double == False

def test_parse_bar_double2(bar2):
    assert bar2.double == True


# parse_tandem

def test_parse_tandem_clef():
    assert main.parse_tandem("*clefG").data == "treble"

def test_parse_tandem_instr_class():
    assert main.parse_tandem("*ICvox").data == "vox"

def test_parse_tandem_instr_group():
    assert main.parse_tandem("*IGsolo").data == "solo"

def test_parse_tandem_instr_name_user():
    assert main.parse_tandem("*I:violin 1").data == "violin 1"

def test_parse_tandem_instr_name_default():
    assert main.parse_tandem("*Isoprn").data == "soprn"

def test_parse_tandem_key_sig_sharp():
    assert main.parse_tandem("*k[f#c#]").data == 2

def test_parse_tandem_key_sig_flat():
    assert main.parse_tandem("*k[B-E-]").data == -2

def test_parse_tandem_key_sig_bartok():
    assert main.parse_tandem("*k[B-F#]").data == ["bb", "f#"]

def test_parse_tandem_tempo():
    assert main.parse_tandem("*MM88.97").data == 88.97

def test_parse_tandem_meter():
    assert main.parse_tandem("*M6/8").data == "6/8"

def test_parse_tandem_timebase():
    assert main.parse_tandem("*tb32").data == 32.0

def test_parse_tandem_transposing_instrument():
    assert main.parse_tandem("*ITrd1c2").data == "d1c2"

def test_parse_tandem_repetition():
    assert main.parse_tandem("*>[aria1,aria2]").data == ["aria1", "aria2"]

def test_parse_tandem_label():
    assert main.parse_tandem("*>aria").data == "aria"

def test_parse_tandem_key():
    assert main.parse_tandem("*A-:").data == "Ab"


# parse_item

def test_parse_item_list():
    item = main.parse_item(["**kern", "**kern"], score.Score())
    assert [x.name for x in item] == ["kern", "kern"]

def test_parse_item_bar():
    item = main.parse_item("=2:||:", score.Score())
    assert isinstance(item, score.Bar)

def test_parse_item_einterp():
    item = main.parse_item("**kern", score.Score())
    assert isinstance(item, score.Exclusive)

def test_parse_item_tandem():
    item = main.parse_item("*ClefF4", score.Score())
    assert isinstance(item, score.Tandem)

def test_parse_item_tandem_spine_names_from_user_instrument():
    sco = score.Score()
    main.parse_item("*I:violin 1", sco)
    assert sco.spine_names == ["violin 1"]

def test_parse_item_tandem_spine_names_from_instrument():
    sco = score.Score()
    main.parse_item("*Iviolin", sco)
    assert sco.spine_names == ["violin"]

def test_parse_item_comment():
    item = main.parse_item("! foo", score.Score())
    assert isinstance(item, score.Comment)

def test_parse_item_null_interpretation():
    item = main.parse_item("*", score.Score())
    assert isinstance(item, score.NullInterpretation)

def test_parse_item_null():
    item = main.parse_item(".", score.Score())
    assert isinstance(item, score.NullToken)


# parse_reference_record

def pytest_funcarg__record(request):
    return main.parse_reference_record("!!! COM: J. S. Bach")


def test_parse_reference_record_name(record):
    assert record.name == 'COM'

def test_parse_reference_record_data(record):
    assert record.data == 'J. S. Bach'


# parse_comment

def test_parse_comment_simple():
    assert main.parse_comment("!! foobar").data == "foobar"

def test_parse_comment_with_exclamation():
    assert main.parse_comment("!! foobar!").data == "foobar!"


# parse_line

# parse_line can't parse a single line like '4c f' without context
# because parse_line doesn't know the type of the spines. When
# parse_line parses a line like '**kern' it will store the spine type
# in score.spine_types. At this stage the best we can do is to parse
# reference records, global comments, single lines, and exclusive
# interpretation. If you want to parse things like kern data, you
# should use parse_kern_item instead.


def test_parse_line_composer():
    f = main.parse_line("!!!COM: Pedro Kroger", score.Score())
    assert f.composer == 'Pedro Kroger'

def test_parse_line_title():
    f = main.parse_line("!!!OTL: My Music", score.Score())
    assert f.title == 'My Music'

def test_parse_line_record():
    f = main.parse_line("!! Global comment", score.Score())
    assert isinstance(f[0], score.Comment)

def test_parse_line_blankline():
    # FIXME: is this a bug?
    f = main.parse_line("", score.Score())
    assert isinstance(f[0], score.BlankLine)


def pytest_funcarg__line1(request):
    return main.parse_line("**kern\t**kern", score.Score())

def test_parse_line_exclusive_spine1(line1):
    assert isinstance(line1[0][0], score.Exclusive)

def test_parse_line_exclusive_spine2(line1):
    assert isinstance(line1[0][1], score.Exclusive)

def test_parse_error_no_prev_information():
    py.test.raises(main.HumdrumError, main.parse_line, "4c	f", score.Score())


def pytest_funcarg__score_line(request):
    s = score.Score()
    main.parse_line("**kern	**kern", s)
    main.parse_line("4c	4d", s)
    return s

def test_parse_line_exclusive_spine1(score_line):
    assert isinstance(score_line[0][0], score.Exclusive)

def test_parse_line_exclusive_spine2(score_line):
    assert isinstance(score_line[0][1], score.Exclusive)

def test_parse_line_note_spine1(score_line):
    assert isinstance(score_line[1][0], score.Note)

def test_parse_line_note_spine2(score_line):
    assert isinstance(score_line[1][1], score.Note)


def pytest_funcarg__line_comments(request):
    return main.parse_line("!foo\t!! bar", score.Score())

def test_parse_line_data_spine1(line_comments):
    assert line_comments[0][0].data == "foo"

def test_parse_line_data_spine2(line_comments):
    assert line_comments[0][1].data == "bar"

def test_parse_line_level_spine1(line_comments):
    assert line_comments[0][0].level == 1

def test_parse_line_level_spine2(line_comments):
    assert line_comments[0][1].level == 2


# parse_string

def pytest_funcarg__simple_score(request):
    return main.parse_string("**kern\n4c\n*-")


def test_parse_string_spine_types():
    sco1 = main.parse_string("**kern\t**kern\nc4\tc4\n*-\t*-")
    assert sco1.spine_types == ['kern', 'kern']

# We check if the basics of parse_string are working by parsing a
# string with 3 elements (only one spine) and checking the type of
# each element.

def test_parse_string_number_elements(simple_score):
    assert 3 == len(simple_score)

def test_parse_string_exclusive(simple_score):
    assert isinstance(simple_score[0][0], score.Exclusive)

def test_parse_string_note(simple_score):
    assert isinstance(simple_score[1][0], score.Note)

def test_parse_string_spine_path(simple_score):
    assert isinstance(simple_score[2][0], score.SpinePath)

# test parsing a string with different note systems

def test_parse_string_base12():
    sco = main.parse_string("**kern\n4e-\n*-", note_system="base12")
    note = sco[1][0]
    assert note.code == 3

def test_parse_string_base40():
    sco = main.parse_string("**kern\n4c\n*-", note_system="base40")
    note = sco[1][0]
    assert note.code == 3

def test_parse_string_midi():
    sco = main.parse_string("**kern\n4e-\n*-", note_system="midi")
    note = sco[1][0]
    assert note.code == 63

# test parsing a non-kern spine

def pytest_funcarg__foo_spine(request):
    return main.parse_string("**foo\nbar\n*-")

def test_parse_non_kern_spine_name(foo_spine):
    assert foo_spine[0][0].name == 'foo'

def test_parse_non_kern_spine_value(foo_spine):
    assert foo_spine[1][0] == 'bar'

# parse file

def test_parse_file():
    temp = tempfile.NamedTemporaryFile(mode='w+t')

    try:
        temp.writelines("**kern")
        temp.seek(0)
        sco = main.parse_file(temp.name)
        assert  sco[0][0].name == "kern"
    finally:
        temp.close()
