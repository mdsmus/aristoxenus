from aristoxenus import utils
import py

# search_string

def test_replace_flats():
    assert utils.replace_flats("CC--") == "CCbb"

def test_search_string_foo_in_foobar():
    assert utils.search_string("^foo", "foobar") == "foo"

def test_search_string_numbers_in_foobar():
    assert utils.search_string("[0-9]+", "foobar") == None

def test_flatten_one_level():
    assert list(utils.flatten([[1, 2], [4, 5]])) == [1, 2, 4, 5]

def test_flatten_two_levels():
    assert list(utils.flatten([[1, 2, [3, 3]], [4, 5]])) == [1, 2, 3, 3, 4, 5]

def test_flatten_two_levels_and_empty_list():
    assert list(utils.flatten([[1, 2, []], [4, 5]])) == [1, 2, 4, 5]

def test_flatten_three_levels():
    big_list = [[1, 2, [3, [4, 5]]], [6, [[7, 8]], 9]]
    assert list(utils.flatten(big_list)) == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def pytest_funcarg__visitor_show(request):
    class PrintVisitor(utils.Visitor):
        def visit_Foo(self, obj):
            return 'visiting foo'

        def visit_Bar(self, obj):
            return 'visiting bar'

    def show(obj):
        p = PrintVisitor()
        return p.dispatch(obj)

    return show


def test_visitor_foo(visitor_show):
    class Foo(): pass
    a = Foo()
    assert visitor_show(a) == "visiting foo"

def test_visitor_bar(visitor_show):
    class Bar(): pass
    b = Bar()
    assert visitor_show(b) == "visiting bar"

def test_visitor_default(visitor_show):
    py.test.raises(utils.VisitorError, visitor_show, 10)
