import utils
from unittest import TestCase

class TestUtils(TestCase):
    def test_search_string(self):
        self.assertTrue(utils.search_string("^foo", "foobar"))
        self.assertFalse(utils.search_string("[0-9]+", "foobar"))
