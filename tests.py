#!/usr/bin/env python2.6

import humdrum
import unittest


class TestBasicParsing(unittest.TestCase):
    def test_parse_global_comment(self):
        result = humdrum.parse_global_comment("!!! foo")
        self.assertTrue(isinstance(result, humdrum.Comment))


if __name__ == '__main__':
    unittest.main()
