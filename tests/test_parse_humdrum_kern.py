import aristoxenus.parse.humdrum.kern as kern
from aristoxenus import score
from fractions import Fraction
import py


# parse_kern_note

def test_parse_kern_note_D2s():
    assert kern.parse_kern_note('ddd', '##') == "D##"

def test_parse_kern_note_C3s():
    assert kern.parse_kern_note('ccc', '###') == "C###"

def test_parse_kern_note_E2f():
    assert kern.parse_kern_note('eee', '--') == "Ebb"

def test_parse_kern_note_E():
    assert kern.parse_kern_note('e', '') == "E"


# parse_kern_octave

def test_parse_kern_octave_EEEs():
    assert kern.parse_kern_octave('EEE', '#') == 1

def test_parse_kern_octave_DD():
    assert kern.parse_kern_octave('DD', '') == 2

def test_parse_kern_octave_CC():
    assert kern.parse_kern_octave('CC', '') == 2

def test_parse_kern_octave_C():
    assert kern.parse_kern_octave('C', '') == 3

def test_parse_kern_octave_c():
    assert kern.parse_kern_octave('c', '') == 4

def test_parse_kern_octave_dd():
    assert kern.parse_kern_octave('dd', '') == 5

def test_parse_kern_octave_eees():
    assert kern.parse_kern_octave('eee', '#') == 6

def test_parse_kern_octave_eee2s():
    assert kern.parse_kern_octave('eee', '##') == 6

def test_parse_kern_octave_eee3s():
    assert kern.parse_kern_octave('eee', '###') == 6

def test_parse_kern_octave_FF2f():
    assert kern.parse_kern_octave('FF', '--') == 2

def test_parse_kern_octave_GGGs():
    assert kern.parse_kern_octave('GGG', '#') == 1

# a few boundary cases, where accidentals change the octave

def test_parse_kern_octave_cf():
    assert kern.parse_kern_octave('c', '-') == 3

def test_parse_kern_octave_d3f():
    assert kern.parse_kern_octave('d', '---') == 3

def test_parse_kern_octave_bs():
    assert kern.parse_kern_octave('b', '#') == 5

def test_parse_kern_octave_Cf():
    assert kern.parse_kern_octave('C', '-') == 2

def test_parse_kern_octave_D3f():
    assert kern.parse_kern_octave('D', '---') == 2

def test_parse_kern_octave_Bs():
    assert kern.parse_kern_octave('B', '#') == 4

def test_parse_kern_octave_error_CCCCC():
    py.test.raises(AssertionError, kern.parse_kern_octave, 'CCCCC', '')

def test_parse_kern_octave_error_empty():
    py.test.raises(kern.KernError, kern.parse_kern_octave, '', '')


# kern_tokenizer

def pytest_funcarg__token1(request):
    return kern.kern_tokenizer("4.cc##Pq")

def test_kern_tokenizer_note(token1):
    assert token1['note'] == ['c', 'c']

def test_kern_tokenizer_acc(token1):
    assert token1['acc'] == ['#', '#']

def test_kern_tokenizer_app(token1):
    assert token1['app'] == ['P']

def test_kern_tokenizer_app(token1):
    assert token1['acciac'] == ['q']

def test_kern_tokenizer_dur(token1):
    assert token1['dur'] == ['4']

def test_kern_tokenizer_dot(token1):
    assert token1['dot'] == ['.']


# parse_kern_item

def pytest_funcarg__note1(request):
    return kern.parse_kern_item("4c")

def pytest_funcarg__note2(request):
    return kern.parse_kern_item("4.CC##T;U(L")


def test_parse_kern_item_name(note1):
    assert note1.name == 'C'

def test_parse_kern_item_duration_0():
    note = kern.parse_kern_item("0c")
    assert note.duration == 2

def test_parse_kern_item_duration_1():
    note = kern.parse_kern_item("1c")
    assert note.duration == Fraction(1, 1)

def test_parse_kern_item_duration_2():
    note = kern.parse_kern_item("2c")
    assert note.duration == Fraction(1, 2)

def test_parse_kern_item_duration_4():
    note = kern.parse_kern_item("4c")
    assert note.duration == Fraction(1, 4)

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
    assert note2.duration == Fraction(3, 8)

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


def test_parse_kern_item_error_no_note_or_rest():
    py.test.raises(kern.KernError, kern.parse_kern, "4y")

def test_parse_kern_item_error_no_note_and_rest():
    py.test.raises(kern.KernError, kern.parse_kern, "4rc")

def test_parse_kern_item_error_no_duration():
    py.test.raises(kern.KernError, kern.parse_kern, "co")


# parse_kern

def test_parse_kern_4c():
    assert isinstance(kern.parse_kern("4c"), score.Note)

def test_parse_kern_4r():
    assert isinstance(kern.parse_kern("4r"), score.Rest)

def test_parse_kern_4c_base40():
    assert kern.parse_kern("4c").code == 3

def test_parse_kern_4c_base12():
    assert kern.parse_kern("4c", note_system="base12").code == 0

def test_parse_kern_double_stops():
    assert isinstance(kern.parse_kern("4c 4c"), score.MultipleStop)

def test_parse_kern_empty():
    py.test.raises(kern.KernError, kern.parse_kern, "")
