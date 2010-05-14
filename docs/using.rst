Using Aristoxenus
=================

Aristoxenus is a library and not a full program, but it makes it easy
for you to develop python programs with music intelligence.

Processing humdrum data
-----------------------

To process humdrum files the first thing you need to do is to parse a
humdrum file with :func:`aristoxenus.parse.humdrum.main.parse_file`.
It will return an object of type :class:`aristoxenus.score.Score`.
Since Score is the main data structure in Aristoxenus, you should
familiarize with it. The section :ref:`score` provides a good
introduction.

The function :func:`aristoxenus.emit.humdrum.show` can be used to
print a :class:`Score()` as a humdrum file. In the following
example, we parse a humdrum file called "foo.krn" and print only the
first spine::

    from aristoxenus import parse
    from aristoxenus import emit
    from aristoxenus import score

    sco = parse.humdrum.parse_file("foo.krn")
    data = sco.get_spine(0)
    print emit.humdrum.show(score.Score(*data))

The following example is a little bit more elaborate. We'll build a
tool similar to humdrum's extract.

.. literalinclude:: examples/extract.py
