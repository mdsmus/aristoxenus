import utils


def test_search_string():
    assert utils.search_string("^foo", "foobar") == True
    assert utils.search_string("[0-9]+", "foobar") == False
