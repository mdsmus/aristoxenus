from fractions import Fraction
import score
import convert


def test_show_as_humdrum():
    record = score.Record("COM", "J. S. Bach")
    comment = score.Comment("bla bla", 2)
    #tandem = score.Tandem()
    exclusive = score.Exclusive("kern")
    note1 = score.Note("C#", Fraction(1, 4))
    note1.octave = 7
    note2 = score.Note("Cbb", Fraction(3, 8))
    note2.octave = 3
    note3 = score.Note("C", Fraction(1, 4))
    note3.articulations = ["harmonic", "turn", "tie-start"]
    chord = score.MultipleStop([note1, note2])
    bar = score.Bar(2)
    rest = score.Rest(Fraction(3, 8))
    blank = score.BlankLine()
    null = score.NullToken()
    unknowntype = score.UnknownType("foo")
    assert convert.show_as_humdrum(record) == '!!! COM: J. S. Bach'
    assert convert.show_as_humdrum(comment) == '!! bla bla'
    #assert convert.show_as_humdrum(Tandem) == '!! bla bla'
    assert convert.show_as_humdrum(exclusive) == "**kern"
    assert convert.show_as_humdrum(note1) == "4cccc#"
    assert convert.show_as_humdrum(note2) == "4.C--"
    assert convert.show_as_humdrum(note3) == "4coS["
    assert convert.show_as_humdrum(chord) == "4cccc# 4.C--"
    assert convert.show_as_humdrum(bar) == "=2"
    assert convert.show_as_humdrum(rest) == "4.r"
    assert convert.show_as_humdrum(blank) == "\n"
    assert convert.show_as_humdrum(null) == "."
    assert convert.show_as_humdrum(unknowntype) == "foo"
