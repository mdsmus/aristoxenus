from xenophilus import humdrum as h
from unittest import TestCase
from fractions import Fraction as frac


class TestScore(TestCase):
    def test_append(self):
        score = h.Score()
        score.append("foo")
        self.assertEqual(["foo"], score.data)

class TestRecord(TestCase):
    def test___init__(self):
        # record = Record(name, data)
        assert False # TODO: implement your test here

class TestComment(TestCase):
    def test___init__(self):
        # comment = Comment(data)
        assert False # TODO: implement your test here

class TestTandem(TestCase):
    def test___init__(self):
        # tandem = Tandem(spine_type, data)
        assert False # TODO: implement your test here

class TestExclusiveInterpretation(TestCase):
    def test___init__(self):
        # exclusive_interpretation = ExclusiveInterpretation(name)
        assert False # TODO: implement your test here

    def test___repr__(self):
        # exclusive_interpretation = ExclusiveInterpretation(name)
        # self.assertEqual(expected, exclusive_interpretation.__repr__())
        assert False # TODO: implement your test here

class TestNote(TestCase):
    def test___init__(self):
        # note = Note(name, dur, art, beams, octave, code, system, spinetype)
        assert False # TODO: implement your test here

class TestMultipleStop(TestCase):
    def test___repr__(self):
        # multiple_stop = MultipleStop()
        # self.assertEqual(expected, multiple_stop.__repr__())
        assert False # TODO: implement your test here

class TestBar(TestCase):
    def test___init__(self):
        # bar = Bar(number, repeat_begin, repeat_end, double)
        assert False # TODO: implement your test here

class TestRest(TestCase):
    def test___init__(self):
        # rest = Rest(dur, wholeNote)
        assert False # TODO: implement your test here

class TestKernError(TestCase):
    def test_kern_error(self):
        # self.assertEqual(expected, kern_error(message))
        assert False # TODO: implement your test here

class TestParseKernNote(TestCase):
    def test_parse_kern_note(self):
        # self.assertEqual(expected, parse_kern_note(note, accs, lineno))
        assert False # TODO: implement your test here

class TestParseKernOctave(TestCase):
    def test_parse_kern_octave(self):
        # self.assertEqual(expected, parse_kern_octave(note, lineno))
        assert False # TODO: implement your test here

class TestKernTokenizer(TestCase):
    def test_kern_tokenizer(self):
        # self.assertEqual(expected, kern_tokenizer(token, linen))
        assert False # TODO: implement your test here

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
        # self.assertEqual(expected, parse_dynam(item, lineno, itemno))
        assert False # TODO: implement your test here


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
        # self.assertEqual(expected, parse_tandem(item))
        assert False # TODO: implement your test here


class TestParseItem(TestCase):
    def test_parse_item_bar(self):
        item = h.parse_item("=2:||:", 1, 1, h.Score())
        self.assertTrue(isinstance(item, h.Bar))

    def test_parse_item_einterp(self):
        item = h.parse_item("**kern", 1, 1, h.Score())
        self.assertTrue(isinstance(item, h.ExclusiveInterpretation))

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
        f = h.parse_comment("!! foobar")
        self.assertEqual("foobar", f.data)


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
        self.assertTrue(isinstance(f.data[0], h.ExclusiveInterpretation))
        self.assertTrue(isinstance(f.data[1], h.ExclusiveInterpretation))
         
    def test_parse_line5(self):
        line = "4c	f"
        score = h.Score()
        self.assertRaises(h.KernError, lambda: h.parse_line(line, score, 1))
         
    def test_parse_line6(self):
        score = h.Score()
        h.parse_line("**kern	**kern", score, 1)
        h.parse_line("4c	4d", score, 1)
        self.assertTrue(isinstance(score.data[0][0], h.ExclusiveInterpretation))
        self.assertTrue(isinstance(score.data[0][1], h.ExclusiveInterpretation))
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
        self.assertTrue(isinstance(self.data[0][0], h.ExclusiveInterpretation))
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
        self.assertTrue(isinstance(data[0][0], h.ExclusiveInterpretation))
        self.assertTrue(isinstance(data[1][0], h.Note))
        self.assertTrue(isinstance(data[2][0], h.Tandem))


if __name__ == '__main__':
    unittest.main()
