from fractions import Fraction as frac
from aristoxenus import score

# Simple tests to make sure the main classes are instantiating
# correctly and without errors. Most classes will be tested in the
# other tests in this suite, but it's good to have these simple tests
# in case some class end up not being tested.

def pytest_funcarg__item_score(request):
    sco = score.Score()
    sco.append("foo")
    return sco


def test_score_append(item_score):
    assert item_score == ["foo"]

def test_score_is_a_score(item_score):
    assert isinstance(item_score, score.Score)

def test_score_is_a_list():
    assert score.Score(1, 2, 3) == [1, 2, 3]

def test_score_record():
    record = score.Record("COM", "J. S. Bach")
    assert isinstance(record, score.Record)

def test_score_comment():
    comment = score.Comment("Foobar", 2)
    assert isinstance(comment, score.Comment)

def test_score_tandem():
    tandem = score.Tandem("Clef", "C4")
    assert isinstance(tandem, score.Tandem)

def test_score_exclusive():
    exinterp = score.Exclusive("kern")
    assert isinstance(exinterp, score.Exclusive)

def test_score_note():
    note = score.Note("c##", frac(1, 4))
    assert isinstance(note, score.Note)

def test_score_multiple_stop():
    multiple_stop = score.MultipleStop()
    assert isinstance(multiple_stop, score.MultipleStop)

def test_score_bar():
    bar = score.Bar(1)
    assert isinstance(bar, score.Bar)

def test_score_rest():
    rest = score.Rest(frac(1, 4))
    assert isinstance(rest, score.Rest)
