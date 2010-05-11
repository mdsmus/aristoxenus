import humdrum as h
import score
from fractions import Fraction as frac
import py


# parse_kern_note

def test_parse_kern_note_D2s():
    assert h.parse_kern_note('ddd', '##') == "D##"

def test_parse_kern_note_C3s():
    assert h.parse_kern_note('ccc', '###') == "C###"

def test_parse_kern_note_E2f():
    assert h.parse_kern_note('eee', '--') == "Ebb"

def test_parse_kern_note_E():
    assert h.parse_kern_note('e', '') == "E"


# parse_kern_octave

def test_parse_kern_octave_EEEs():
    assert h.parse_kern_octave('EEE', '#') == 1

def test_parse_kern_octave_DD():
    assert h.parse_kern_octave('DD', '') == 2

def test_parse_kern_octave_CC():
    assert h.parse_kern_octave('CC', '') == 2

def test_parse_kern_octave_C():
    assert h.parse_kern_octave('C', '') == 3

def test_parse_kern_octave_c():
    assert h.parse_kern_octave('c', '') == 4

def test_parse_kern_octave_dd():
    assert h.parse_kern_octave('dd', '') == 5

def test_parse_kern_octave_eees():
    assert h.parse_kern_octave('eee', '#') == 6

def test_parse_kern_octave_eee2s():
    assert h.parse_kern_octave('eee', '##') == 6

def test_parse_kern_octave_eee3s():
    assert h.parse_kern_octave('eee', '###') == 6

def test_parse_kern_octave_FF2f():
    assert h.parse_kern_octave('FF', '--') == 2

def test_parse_kern_octave_GGGs():
    assert h.parse_kern_octave('GGG', '#') == 1

# a few boundary cases, where accidentals change the octave

def test_parse_kern_octave_cf():
    assert h.parse_kern_octave('c', '-') == 3

def test_parse_kern_octave_d3f():
    assert h.parse_kern_octave('d', '---') == 3

def test_parse_kern_octave_bs():
    assert h.parse_kern_octave('b', '#') == 5

def test_parse_kern_octave_Cf():
    assert h.parse_kern_octave('C', '-') == 2

def test_parse_kern_octave_D3f():
    assert h.parse_kern_octave('D', '---') == 2

def test_parse_kern_octave_Bs():
    assert h.parse_kern_octave('B', '#') == 4

def test_parse_kern_octave_error_CCCCC():
    py.test.raises(AssertionError, h.parse_kern_octave, 'CCCCC', '')

def test_parse_kern_octave_error_empty():
    py.test.raises(h.KernError, h.parse_kern_octave, '', '')


# kern_tokenizer

def pytest_funcarg__token1(request):
    return h.kern_tokenizer("4.cc##")

def test_kern_tokenizer_note(token1):
    assert token1['note'] == ['c', 'c']

def test_kern_tokenizer_acc(token1):
    assert token1['acc'] == ['#', '#']

def test_kern_tokenizer_dur(token1):
    assert token1['dur'] == ['4']

def test_kern_tokenizer_dot(token1):
    assert token1['dot'] == ['.']


# parse_kern_item

def pytest_funcarg__note1(request):
    return h.parse_kern_item("4c")

def pytest_funcarg__note2(request):
    return h.parse_kern_item("4.CC##T;U(L")


def test_parse_kern_item_name(note1):
    assert note1.name == 'C'

def test_parse_kern_item_duration(note1):
    assert note1.duration == frac(1, 4)

def test_parse_kern_item_octave(note1):
    assert note1.octave == 4

def test_parse_kern_item_code(note1):
    assert note1.code == 3

def test_parse_kern_item_system(note1):
    assert note1.system == "base40"

def test_parse_kern_item_type(note1):
    assert note1.type == "kern"


def test_parse_kern_item2_name(note2):
    assert note2.name == 'C##'

def test_parse_kern_item2_duration(note2):
    assert note2.duration == frac(3, 8)

def test_parse_kern_item2_octave(note2):
    assert note2.octave == 2

def test_parse_kern_item2_code(note2):
    assert note2.code == 5

def test_parse_kern_item2_system(note2):
    assert note2.system == "base40"

def test_parse_kern_item2_type(note2):
    assert note2.type == "kern"

def test_parse_kern_item2_articulations_trill(note2):
    assert 'trill-wt' in note2.articulations

def test_parse_kern_item2_articulations_fermata(note2):
    assert 'fermata' in note2.articulations

def test_parse_kern_item2_articulations_mute(note2):
    assert 'mute' in note2.articulations

def test_parse_kern_item2_articulations_slur(note2):
    assert 'slur-start', note2.articulations

def test_parse_kern_item2_articulations_beam(note2):
    assert 'beam-start', note2.beams


# parse_kern

def test_parse_kern_4c():
    assert isinstance(h.parse_kern("4c"), score.Note)

def test_parse_kern_4r():
    assert isinstance(h.parse_kern("4r"), score.Rest)


# parse_bar

def pytest_funcarg__bar1(request):
    return h.parse_bar("=2:||:")

def pytest_funcarg__bar2(request):
    return h.parse_bar("==2")


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
    assert h.parse_tandem("*clefG").data == "treble"

def test_parse_tandem_instr_class():
    assert h.parse_tandem("*ICvox").data == "vox"

def test_parse_tandem_instr_group():
    assert h.parse_tandem("*IGsolo").data == "solo"

def test_parse_tandem_instr_name_user():
    assert h.parse_tandem("*I:violin 1").data == "violin 1"

def test_parse_tandem_instr_name_default():
    assert h.parse_tandem("*Isoprn").data == "soprn"

def test_parse_tandem_key_sig_sharp():
    assert h.parse_tandem("*k[f#c#]").data == 2

def test_parse_tandem_key_sig_flat():
    assert h.parse_tandem("*k[B-E-]").data == -2

def test_parse_tandem_tempo():
    assert h.parse_tandem("*MM88.97").data == 88.97

def test_parse_tandem_meter():
    assert h.parse_tandem("*M6/8").data == "6/8"

def test_parse_tandem_timebase():
    assert h.parse_tandem("*tb32").data == 32.0

def test_parse_tandem_transposing_instrument():
    assert h.parse_tandem("*ITrd1c2").data == "d1c2"

def test_parse_tandem_repetition():
    assert h.parse_tandem("*>[aria1,aria2]").data == ["aria1", "aria2"]

def test_parse_tandem_label():
    assert h.parse_tandem("*>aria").data == "aria"

def test_parse_tandem_key():
    assert h.parse_tandem("*A-:").data == "Ab"


# parse_item

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


# parse_reference_record

def pytest_funcarg__record(request):
    return h.parse_reference_record("!!! COM: J. S. Bach")


def test_parse_reference_record_name(record):
    assert record.name == 'COM'

def test_parse_reference_record_data(record):
    assert record.data == 'J. S. Bach'


# parse_comment

def test_parse_comment_simple():
    assert h.parse_comment("!! foobar").data == "foobar"

def test_parse_comment_with_exclamation():
    assert h.parse_comment("!! foobar!").data == "foobar!"


# parse_line

# parse_line can't parse a single line like '4c f' without context
# because parse_line doesn't know the type of the spines. When
# parse_line parses a line like '**kern' it will store the spine type
# in score.spine_types. At this stage the best we can do is to parse
# reference records, global comments, single lines, and exclusive
# interpretation. If you want to parse things like kern data, you
# should use parse_kern_item instead.


def test_parse_line_record():
    f = h.parse_line("!!!com: Pedro Kroger", score.Score())
    assert isinstance(f[0], score.Record)

def test_parse_line_record():
    f = h.parse_line("!! Global comment", score.Score())
    assert isinstance(f[0], score.Comment)

def test_parse_line_blankline():
    # FIXME: is this a bug?
    f = h.parse_line("", score.Score())
    assert isinstance(f[0], score.BlankLine)


def pytest_funcarg__line1(request):
    return h.parse_line("**kern\t**kern", score.Score())

def test_parse_line_exclusive_spine1(line1):
    assert isinstance(line1[0][0], score.Exclusive)

def test_parse_line_exclusive_spine2(line1):
    assert isinstance(line1[0][1], score.Exclusive)

def test_parse_error_no_prev_information():
    py.test.raises(h.KernError, h.parse_line, "4c	f", score.Score())


def pytest_funcarg__score_line(request):
    s = score.Score()
    h.parse_line("**kern	**kern", s)
    h.parse_line("4c	4d", s)
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
    return h.parse_line("!foo\t!! bar", score.Score())

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
    return h.parse_string("**kern\n4c\n*-")


def test_parse_string_spine_types():
    sco1 = h.parse_string("**kern\t**kern\nc4\tc4\n*-\t*-")
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
