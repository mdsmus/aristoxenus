import score
from fractions import Fraction as frac


def test_score():
    """Simple tests to make sure the main classes are
    instantiating correctly and without errors. Most classes will
    be tested in the other tests in this suite, but it's good to
    have these simple tests in case some class end up not being
    tested.
    """

    s = score.Score()
    s.append("foo")

    record = score.Record("COM", "J. S. Bach")
    comment = score.Comment("Foobar")
    tandem = score.Tandem("Clef", "C4")
    exinterp = score.Exclusive("kern")
    note = score.Note("c##", frac(1, 4))
    score.octave = 6
    score.code = 5
    score.system = "base40"
    score.type = "kern"
    multiple_stop = score.MultipleStop()
    bar = score.Bar(1)
    rest = score.Rest(frac(1, 4))

    assert s.data == ["foo"]
    assert isinstance(s, score.Score)
    assert isinstance(record, score.Record)
    assert isinstance(comment, score.Comment)
    assert isinstance(tandem, score.Tandem)
    assert isinstance(exinterp, score.Exclusive)
    assert isinstance(note, score.Note)
    assert isinstance(multiple_stop, score.MultipleStop)
    assert isinstance(bar, score.Bar)
    assert isinstance(rest, score.Rest)
