import unittest
from xenophilus import humdrum

class TestParseKernNote(unittest.TestCase):
    def test_parse_kern_note(self):
        # self.assertEqual(expected, parse_kern_note(note, accs, lineno))
        assert False # TODO: implement your test here

class TestParseKernOctave(unittest.TestCase):
    def test_parse_kern_octave(self):
        # self.assertEqual(expected, parse_kern_octave(note, lineno))
        assert False # TODO: implement your test here

class TestKernTokenizer(unittest.TestCase):
    def test_kern_tokenizer(self):
        # self.assertEqual(expected, kern_tokenizer(string, linen))
        assert False # TODO: implement your test here

class TestParseKernItem(unittest.TestCase):
    def test_parse_kern_item(self):
        # self.assertEqual(expected, parse_kern_item(string, lineno, itemno))
        assert False # TODO: implement your test here

class TestParseKern(unittest.TestCase):
    def test_parse_kern(self):
        # self.assertEqual(expected, parse_kern(string, linen, itemno))
        assert False # TODO: implement your test here

class TestParseDynam(unittest.TestCase):
    def test_parse_dynam(self):
        # self.assertEqual(expected, parse_dynam(string, lineno, itemno))
        assert False # TODO: implement your test here

class TestUnknownType(unittest.TestCase):
    def test_unknown_type(self):
        # self.assertEqual(expected, unknown_type(item, lineno, itemno))
        assert False # TODO: implement your test here

class TestParseBar(unittest.TestCase):
    def test_parse_bar(self):
        # self.assertEqual(expected, parse_bar(string))
        assert False # TODO: implement your test here

class TestParseTandem(unittest.TestCase):
    def test_parse_tandem(self):
        # self.assertEqual(expected, parse_tandem(string))
        assert False # TODO: implement your test here

class TestParseData(unittest.TestCase):
    def test_parse_data(self):
        # self.assertEqual(expected, parse_data(item, lineno, itemno, data_type))
        assert False # TODO: implement your test here

class TestParseSpineItem(unittest.TestCase):
    def test_parse_spine_item(self):
        # self.assertEqual(expected, parse_spine_item(item, lineno, itemno, score))
        assert False # TODO: implement your test here

class TestParseReferenceRecord(unittest.TestCase):
    def test_parse_reference_record(self):
        # self.assertEqual(expected, parse_reference_record(line))
        assert False # TODO: implement your test here

class TestParseGlobalComment(unittest.TestCase):
    def test_parse_global_comment(self):
        # self.assertEqual(expected, parse_global_comment(line))
        assert False # TODO: implement your test here

class TestParseSpine(unittest.TestCase):
    def test_parse_spine(self):
        # self.assertEqual(expected, parse_spine(line, lineno, score))
        assert False # TODO: implement your test here

class TestParseLine(unittest.TestCase):
    def test_parse_line(self):
        # self.assertEqual(expected, parse_line(line, score, lineno))
        assert False # TODO: implement your test here

class TestParseString(unittest.TestCase):
    def test_parse_string(self):
        # self.assertEqual(expected, parse_string(string))
        assert False # TODO: implement your test here

class TestParseFile(unittest.TestCase):
    def test_parse_file(self):
        # self.assertEqual(expected, parse_file(file))
        assert False # TODO: implement your test here

class TestBasicParsing(unittest.TestCase):
    def test_parse_global_comment(self):
        result = humdrum.parse_global_comment("!!! foo")
        self.assertTrue(isinstance(result, humdrum.Comment))


if __name__ == '__main__':
    unittest.main()
