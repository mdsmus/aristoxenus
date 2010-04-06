import score
from unittest import TestCase
from fractions import Fraction as frac


class TestScore(TestCase):
    def test_score(self):
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

        self.assertEqual(["foo"], s.data)
        self.assertTrue(isinstance(s, score.Score))
        self.assertTrue(isinstance(record, score.Record))
        self.assertTrue(isinstance(comment, score.Comment))
        self.assertTrue(isinstance(tandem, score.Tandem))
        self.assertTrue(isinstance(exinterp, score.Exclusive))
        self.assertTrue(isinstance(note, score.Note))
        self.assertTrue(isinstance(multiple_stop, score.MultipleStop))
        self.assertTrue(isinstance(bar, score.Bar))
        self.assertTrue(isinstance(rest, score.Rest))


if __name__ == '__main__':
    unittest.main()
