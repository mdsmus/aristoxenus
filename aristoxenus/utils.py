import re
import sys
import itertools


def replace_flats(string):
    return string.replace("-", "b")


def search_string(pattern, string):
    """Like re.search but return the string that matches the pattern
    instead of a Match object."""

    tmp = re.search(pattern, string)
    if tmp:
        return tmp.group()


def flatten(list_of_lists):
    """Flatten a list of list for many levels

    I got it from from http://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
    """

    ltype = type(list_of_lists)
    l = list(list_of_lists)
    i = 0
    while i < len(l):
        while isinstance(l[i], (list, tuple)):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)


class VisitorError(TypeError):
    pass


# FIXME: add arguments and cache
class Visitor():
    """Very simple visitor class.

    To use it you need to subclass the Visitor class and provide
    methods in the form visit_ClassName(self, obj). It's a good idea
    to encapsulate the visitor class in a dispatch function that has a
    relevant name for the application. For instance, to implement a
    printer for the classes Foo() and Bar()::

        class PrintVisitor(Visitor):
            def visit_Foo(self, obj):
                print 'visiting foo'

            def visit_Bar(self, obj):
                print 'visiting bar'

        def show(obj):
            p = PrintVisitor()
            p.dispatch(obj)

    And show() will do the right thing according to the type of object
    it receives::

        a = Foo()
        b = Bar()
        show(a)
        show(b)

    If an object has a type that is not handled by Visitor(), the
    `default` method is called. You can (and should) shadow this
    method when you subclass Visitor.
    """

    def dispatch(self, obj):
        class_name = obj.__class__.__name__
        method = getattr(self, "visit_" + class_name, self.default)
        return method(obj)

    def default(self, obj):
        objtype = type(obj).__name__
        error_string = "No applicable method for object of type "
        raise VisitorError(error_string + objtype)
