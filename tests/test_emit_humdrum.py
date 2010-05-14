from fractions import Fraction
from aristoxenus import emit
from aristoxenus import score

# show

def pytest_funcarg__two_notes(request):
    note1 = score.Note("C#", Fraction(1, 4))
    note1.octave = 7
    note2 = score.Note("Cbb", Fraction(3, 8))
    note2.octave = 3

    return note1, note2


def test_show_record():
    record = score.Record("COM", "J. S. Bach")
    assert emit.humdrum.show(record) == '!!! COM: J. S. Bach'

def test_show_comment():
    comment = score.Comment("bla bla", 2)
    assert emit.humdrum.show(comment) == '!! bla bla'

def test_show_tandem_instrument():
    tandem = score.Tandem("instrument", "violin")
    assert emit.humdrum.show(tandem) == '*Iviolin'

def test_show_tandem_instrument_user():
    tandem = score.Tandem("instrument-user", "violin")
    assert emit.humdrum.show(tandem) == '*I:violin'

def test_show_exclusive():
    exclusive = score.Exclusive("kern")
    assert emit.humdrum.show(exclusive) == "**kern"

def test_show_nullinterpretation():
    assert emit.humdrum.show(score.NullInterpretation()) == '*'

def test_show_spine_end():
    assert emit.humdrum.show(score.SpinePath("spine-end")) == '*-'

def test_show_spine_add():
    assert emit.humdrum.show(score.SpinePath("spine-add")) == '*+'

def test_show_spine_split():
    assert emit.humdrum.show(score.SpinePath("spine-split")) == '*^'

def test_show_spine_join():
    assert emit.humdrum.show(score.SpinePath("spine-join")) == '*v'

def test_show_spine_swap():
    assert emit.humdrum.show(score.SpinePath("spine-swap")) == '*x'

def test_show_note_cs(two_notes):
    note1, note2 = two_notes
    assert emit.humdrum.show(note1) == "4cccc#"

def test_show_note_c2f(two_notes):
    note1, note2 = two_notes
    assert emit.humdrum.show(note2) == "4.C--"

def test_show_note_c_with_articulations():
    note3 = score.Note("C", Fraction(1, 4))
    note3.articulations = ["harmonic", "turn", "tie-start"]
    assert emit.humdrum.show(note3) == "4coS["

def test_show_chord(two_notes):
    note1, note2 = two_notes
    chord = score.MultipleStop([note1, note2])
    assert emit.humdrum.show(chord) == "4cccc# 4.C--"

def test_show_bar():
    bar = score.Bar(2)
    assert emit.humdrum.show(bar) == "=2"

def test_show_rest():
    rest = score.Rest(Fraction(3, 8))
    assert emit.humdrum.show(rest) == "4.r"

def test_show_blankline():
    assert emit.humdrum.show(score.BlankLine()) == "\n"

def test_show_nulltoken():
    assert emit.humdrum.show(score.NullToken()) == "."

def test_show_unknowntype():
    unknowntype = score.UnknownType("foo")
    assert emit.humdrum.show(unknowntype) == "foo"
