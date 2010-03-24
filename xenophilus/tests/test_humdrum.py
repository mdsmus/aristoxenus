from xenophilus import humdrum as h
from unittest import TestCase

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
    def test_parse_kern_item(self):
        # self.assertEqual(expected, parse_kern_item(item, lineno, itemno))
        assert False # TODO: implement your test here

class TestParseKern(TestCase):
    def test_parse_kern(self):
        # self.assertEqual(expected, parse_kern(item, linen, itemno))
        assert False # TODO: implement your test here

class TestParseDynam(TestCase):
    def test_parse_dynam(self):
        # self.assertEqual(expected, parse_dynam(item, lineno, itemno))
        assert False # TODO: implement your test here

class TestUnknownType(TestCase):
    def test_unknown_type(self):
        # self.assertEqual(expected, unknown_type(item, lineno, itemno))
        assert False # TODO: implement your test here

class TestParseBar(TestCase):
    def test_parse_bar(self):
        # self.assertEqual(expected, parse_bar(item))
        assert False # TODO: implement your test here

class TestParseTandem(TestCase):
    def test_parse_tandem(self):
        # self.assertEqual(expected, parse_tandem(item))
        assert False # TODO: implement your test here

class TestParseData(TestCase):
    def test_parse_data(self):
        # self.assertEqual(expected, parse_data(item, lineno, itemno, data_type))
        assert False # TODO: implement your test here

class TestParseItem(TestCase):
    def test_parse_item(self):
        # self.assertEqual(expected, parse_item(item, lineno, itemno, score))
        assert False # TODO: implement your test here

class TestParseReferenceRecord(TestCase):
    def test_parse_reference_record(self):
        # self.assertEqual(expected, parse_reference_record(line))
        assert False # TODO: implement your test here

class TestParseGlobalComment(TestCase):
    def test_parse_global_comment(self):
        # self.assertEqual(expected, parse_global_comment(line))
        assert False # TODO: implement your test here

class TestParseSpine(TestCase):
    def test_parse_spine(self):
        # self.assertEqual(expected, parse_spine(line, lineno, score))
        assert False # TODO: implement your test here

class TestParseLine(TestCase):
    def test_parse_line1(self):
        line = "**kern	**kern"
        score = h.Score()
        self.assertEqual(expected, h.parse_line(line, score, 1))
         
    def test_parse_line2(self):
        f = h.parse_line("", h.Score(), 1)
        self.assertTrue(isinstance(f.data[0], h.BlankLine))
         
    def test_parse_line3(self):
        line = "**kern	**kern"
        f = h.parse_line(line, h.Score(), 1)
        self.assertTrue(isinstance(f.data[0], h.ExclusiveInterpretation))
        self.assertTrue(isinstance(f.data[1], h.ExclusiveInterpretation))
         
    def test_parse_line4(self):
        line = "foobar"
        score = h.Score()
        self.assertRaises(h.KernError, lambda: h.parse_line(line, score, 1))
         
    def test_parse_line5(self):
        line = "4c	."
        score = h.Score()
        self.assertEqual(expected, h.parse_line(line, score, 1))
         

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
