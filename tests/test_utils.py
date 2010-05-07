import utils


def test_search_string():
    assert utils.search_string("^foo", "foobar") == "foo"
    assert utils.search_string("[0-9]+", "foobar") == None
