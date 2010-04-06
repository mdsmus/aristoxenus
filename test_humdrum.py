import humdrum as h
from unittest import TestCase
from fractions import Fraction as frac


class TestClasses(TestCase):
    def test_classes(self):
        """Simple tests to make sure the main classes are
        instantiating correctly and without errors. Most classes will
        be tested in the other tests in this suite, but it's good to
        have these simple tests in case some class end up not being
        tested.
        """

        score = h.Score()
        score.append("foo")

        record = h.Record("COM", "J. S. Bach")
        comment = h.Comment("Foobar")
        tandem = h.Tandem("Clef", "C4")
        exinterp = h.Exclusive("kern")
        note = h.Note("c##", frac(1, 4))
        h.octave = 6
        h.code = 5
        h.system = "base40"
        h.type = "kern"
        multiple_stop = h.MultipleStop()
        bar = h.Bar(1)
        rest = h.Rest(frac(1, 4))

        self.assertEqual(["foo"], score.data)
        self.assertTrue(isinstance(score, h.Score))
        self.assertTrue(isinstance(record, h.Record))
        self.assertTrue(isinstance(comment, h.Comment))
        self.assertTrue(isinstance(tandem, h.Tandem))
        self.assertTrue(isinstance(exinterp, h.Exclusive))
        self.assertTrue(isinstance(note, h.Note))
        self.assertTrue(isinstance(multiple_stop, h.MultipleStop))
        self.assertTrue(isinstance(bar, h.Bar))
        self.assertTrue(isinstance(rest, h.Rest))


class TestParseKernNote(TestCase):
    def test_parse_kern_note(self):
        n1 = h.parse_kern_note(['d', 'd', 'd'], ['#', '#'], 1)
        n2 = h.parse_kern_note(['c', 'c', 'c'], ['#', '#', '#'], 1)
        n3 = h.parse_kern_note(['e', 'e', 'e'], ['-', '-'], 1)
        n4 = h.parse_kern_note(['e'], [], 1)
        self.assertEqual("d##", n1)
        self.assertEqual("c###", n2)
        self.assertEqual("ebb", n3)
        self.assertEqual("e", n4)


class TestParseKernOctave(TestCase):
    def test_parse_kern_octave(self):
        self.assertEqual(4, h.parse_kern_octave("c", 1))
        self.assertEqual(5, h.parse_kern_octave("dd", 1))
        self.assertEqual(6, h.parse_kern_octave("eee#", 1))
        self.assertEqual(6, h.parse_kern_octave("eee##", 1))
        self.assertEqual(6, h.parse_kern_octave("eee###", 1))
        self.assertEqual(3, h.parse_kern_octave("E-", 1))
        self.assertEqual(2, h.parse_kern_octave("FF--", 1))
        self.assertEqual(1, h.parse_kern_octave("GGG#", 1))


class TestKernTokenizer(TestCase):
    def test_kern_tokenizer(self):
        tokens = h.kern_tokenizer("4.cc##", 1)
        self.assertEqual(['c', 'c'], tokens['note'])
        self.assertEqual(['#', '#'], tokens['acc'])
        self.assertEqual(['4'], tokens['dur'])
        self.assertEqual(['.'], tokens['dot'])


class TestParseKernItem(TestCase):
    def test_parse_kern_item1(self):
        n = h.parse_kern_item("4c", 1, 1)
        self.assertEqual('c', n.name)
        self.assertEqual(frac(1, 4), n.duration)
        self.assertEqual(4, n.octave)
        self.assertEqual(3, n.code)
        self.assertEqual("base40", n.system)
        self.assertEqual("kern", n.type)

    def test_parse_kern_item2(self):
        n = h.parse_kern_item("4.CC##T;U(L", 1, 1)
        self.assertEqual('c##', n.name)
        self.assertEqual(frac(3, 8), n.duration)
        self.assertEqual(6, n.octave)
        self.assertEqual(5, n.code)
        self.assertTrue('trill-wt' in n.articulations)
        self.assertTrue('fermata' in n.articulations)
        self.assertTrue('mute' in n.articulations)
        self.assertTrue('slur-start', n.articulations)
        self.assertTrue('beam-start', n.beams)
        self.assertEqual("base40", n.system)
        self.assertEqual("kern", n.type)


class TestParseKern(TestCase):
    def test_parse_kern(self):
        self.assertTrue(isinstance(h.parse_kern("4c", 1, 1), h.Note))
        self.assertTrue(isinstance(h.parse_kern("4r", 1, 1), h.Rest))


class TestParseDynam(TestCase):
    def test_parse_dynam(self):
        self.assertTrue(isinstance(h.parse_dynam("fff", 1, 1), h.Dynam))


class TestParseBar(TestCase):
    def test_parse_bar(self):
        bar = h.parse_bar("=2:||:")
        self.assertEqual(bar.number, "2")
        self.assertEqual(bar.repeat_begin, True)
        self.assertEqual(bar.repeat_end, True)
        self.assertEqual(bar.double, False)
        bar2 = h.parse_bar("==2")
        self.assertEqual(bar2.double, True)


class TestParseTandem(TestCase):
    def test_parse_tandem(self):
        self.assertEqual("fixme, please", parse_tandem("*IVox"))


class TestParseItem(TestCase):
    def test_parse_item_bar(self):
        item = h.parse_item("=2:||:", 1, 1, h.Score())
        self.assertTrue(isinstance(item, h.Bar))

    def test_parse_item_einterp(self):
        item = h.parse_item("**kern", 1, 1, h.Score())
        self.assertTrue(isinstance(item, h.Exclusive))

    def test_parse_item_tandem(self):
        item = h.parse_item("*ClefF4", 1, 1, h.Score())
        self.assertTrue(isinstance(item, h.Tandem))

    def test_parse_item_comment(self):
        item = h.parse_item("! foo", 1, 1, h.Score())
        self.assertTrue(isinstance(item, h.Comment))

    def test_parse_item_null(self):
        item = h.parse_item(".", 1, 1, h.Score())
        self.assertTrue(isinstance(item, h.NullToken))


class TestParseReferenceRecord(TestCase):
    def test_parse_reference_record(self):
        f = h.parse_reference_record("!!! COM: J. S. Bach")

        self.assertEqual(f.name, 'COM')
        self.assertEqual(f.data, 'J. S. Bach')


class TestParseComment(TestCase):
    def test_parse_comment(self):
        c1 = h.parse_comment("!! foobar")
        c2 = h.parse_comment("!! foobar!")
        self.assertEqual("foobar", c1.data)
        self.assertEqual("foobar!", c2.data)


class TestParseLine(TestCase):
    """parse_line can't parse a single line like '4c f' without
    context because parse_line doesn't know the type of the spines.
    When parse_line parses a line like '**kern' it will store the
    spine type in score.spine_types. At this stage the best we can do
    is to parse reference records, global comments, single lines, and
    exclusive interpretation. If you want to parse things like kern
    data, you should use parse_kern_item instead.
    """

    def test_parse_line1(self):
        f = h.parse_line("!!!com: Pedro Kroger", h.Score(), 1)
        self.assertTrue(isinstance(f.data[0], h.Record))

    def test_parse_line2(self):
        f = h.parse_line("!! Global comment", h.Score(), 1)
        self.assertTrue(isinstance(f.data[0], h.Comment))

    def test_parse_line3(self):
        # FIXME: is this a bug?
        f = h.parse_line("", h.Score(), 1)
        self.assertTrue(isinstance(f.data[0], h.BlankLine))

    def test_parse_line4(self):
        line = "**kern	**kern"
        f = h.parse_line(line, h.Score(), 1)
        self.assertTrue(isinstance(f.data[0], h.Exclusive))
        self.assertTrue(isinstance(f.data[1], h.Exclusive))

    def test_parse_line5(self):
        line = "4c	f"
        score = h.Score()
        self.assertRaises(h.KernError, lambda: h.parse_line(line, score, 1))

    def test_parse_line6(self):
        score = h.Score()
        h.parse_line("**kern	**kern", score, 1)
        h.parse_line("4c	4d", score, 1)
        self.assertTrue(isinstance(score.data[0][0], h.Exclusive))
        self.assertTrue(isinstance(score.data[0][1], h.Exclusive))
        self.assertTrue(isinstance(score.data[1][0], h.Note))
        self.assertTrue(isinstance(score.data[1][1], h.Note))


class TestParseString(TestCase):
    """We check if the basics of parse_string are working by parsing a
    string with 3 elements (only one spine) and checking the type of
    each element.
    """

    def setUp(self):
        self.score = h.parse_string("**kern\n4c\n*-")
        self.data = self.score.data

    def test_parse_string(self):
        self.assertEqual(3, len(self.data))
        self.assertTrue(isinstance(self.data[0][0], h.Exclusive))
        self.assertTrue(isinstance(self.data[1][0], h.Note))
        self.assertTrue(isinstance(self.data[2][0], h.Tandem))
        self.assertRaises(AssertionError, lambda: h.parse_string(None))


class TestParseFile(TestCase):
    """We check if the basics of parse_file are working by parsing a
    file with 3 elements (only one spine) and checking the type of
    each element.
    """

    def test_parse_file(self):
        score = h.parse_file("data/simple1.krn")
        data = score.data

        self.assertEqual(3, len(data))
        self.assertTrue(isinstance(data[0][0], h.Exclusive))
        self.assertTrue(isinstance(data[1][0], h.Note))
        self.assertTrue(isinstance(data[2][0], h.Tandem))


if __name__ == '__main__':
    unittest.main()
