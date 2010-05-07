import utils

# search_string

def test_search_string_foo_in_foobar():
    assert utils.search_string("^foo", "foobar") == "foo"

def test_search_string_numbers_in_foobar():
    assert utils.search_string("[0-9]+", "foobar") == None
