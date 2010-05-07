from fractions import Fraction
import score
import convert


# show_as_humdrum

def pytest_funcarg__two_notes(request):
    note1 = score.Note("C#", Fraction(1, 4))
    note1.octave = 7
    note2 = score.Note("Cbb", Fraction(3, 8))
    note2.octave = 3

    return note1, note2


def test_show_as_humdrum_record():
    record = score.Record("COM", "J. S. Bach")
    assert convert.show_as_humdrum(record) == '!!! COM: J. S. Bach'

def test_show_as_humdrum_comment():
    comment = score.Comment("bla bla", 2)
    assert convert.show_as_humdrum(comment) == '!! bla bla'

def test_show_as_humdrum_tandem():
    tandem = score.Tandem("instrument", "violin")
    assert convert.show_as_humdrum(tandem) == '*I:violin'

def test_show_as_humdrum_exclusive():
    exclusive = score.Exclusive("kern")
    assert convert.show_as_humdrum(exclusive) == "**kern"

def test_show_as_humdrum_note_cs(two_notes):
    note1, note2 = two_notes
    assert convert.show_as_humdrum(note1) == "4cccc#"

def test_show_as_humdrum_note_c2f(two_notes):
    note1, note2 = two_notes
    assert convert.show_as_humdrum(note2) == "4.C--"

def test_show_as_humdrum_note_c_with_articulations():
    note3 = score.Note("C", Fraction(1, 4))
    note3.articulations = ["harmonic", "turn", "tie-start"]
    assert convert.show_as_humdrum(note3) == "4coS["

def test_show_as_humdrum_chord(two_notes):
    note1, note2 = two_notes
    chord = score.MultipleStop([note1, note2])
    assert convert.show_as_humdrum(chord) == "4cccc# 4.C--"

def test_show_as_humdrum_bar():
    bar = score.Bar(2)
    assert convert.show_as_humdrum(bar) == "=2"

def test_show_as_humdrum_rest():
    rest = score.Rest(Fraction(3, 8))
    assert convert.show_as_humdrum(rest) == "4.r"

def test_show_as_humdrum_blankline():
    assert convert.show_as_humdrum(score.BlankLine()) == "\n"

def test_show_as_humdrum_nulltoken():
    assert convert.show_as_humdrum(score.NullToken()) == "."

def test_show_as_humdrum_unknowntype():
    unknowntype = score.UnknownType("foo")
    assert convert.show_as_humdrum(unknowntype) == "foo"
