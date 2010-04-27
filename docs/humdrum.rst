The Humdrum parser
==================

Introduction
------------

The humdrum parser described in this document is not 100% strict. This
means that it will extract information from a humdrum file but will
not necessarily give an error if the input contains extra non-valid
data (but it will emit a warning). If you want to check your input for
correctness you should use the ``humdrum`` command (although it will
also disregard a few non-valid input) [#]_. This parser will not allow
things like "a16a", "16a16", "..16", and "16a." but will not check if
the articulations and beams in the respective lists make sense. We are
also assuming that there's only one score per file.

Humdrum files usually have the following elements:

#. global and local comments
#. reference records
#. exclusive interpretation  (``**kern``)
#. tandem interpretation (``*clefF4``)
#. blank lines [#]_
#. data record: (``4.G``)
  #. note
  #. silence
  #. bar
  #. null token
  #. spine path terminator (``*-``)

Here is an example of a music with only one measure::

     !!! reference records
     !! global comments
     **kern
     *Ibass
     *clefF4
     *k[f#]
     *M3/4
     =1
     4G
     4E
     .
     4F#
     *-
     !!! reference records


.. [#] In fact, a kern data like "4c16" will be silently accepted by
       both ``humdrum`` and ``proof``. The humextra tool ``hum2abc``
       will silently ignore the second duration and pick the first (4)
       while the parser described in this document will return an
       error message.

.. [#] Blank lines are not allowed in the humdrum specification and
       ``humdrum`` will output an error, but ``humextras`` and this
       parser allow them because they're useful.

Parsing the Humdrum file format
-------------------------------

The functions :func:`humdrum.parse_file` and
:func:`humdrum.parse_string` are basically a wrapper for
:func:`humdrum.parse_line`.

.. autofunction:: humdrum.parse_file
.. autofunction:: humdrum.parse_string

    >>> parse_string("**kern\n4c\n*-")
    [[<__main__.Exclusive object at 0x7f982d7b3890>],
     [<__main__.Note object at 0x7f982d7b3c10>],
     [<__main__.Tandem object at 0x7f982d7b3fd0>]]

.. autofunction:: humdrum.parse_line

   >>> s = Score()
   >>> parse_line("!! foo bar", s, 1)
   [<__main__.Comment object at 0x7f982d7be1d0>]

   >>> parse_line("!!! foo: bar", s, 1)
   [<__main__.Comment object at 0x7f982d7be1d0>,
    <__main__.Record object at 0x7f982d7be050>]

.. autofunction:: humdrum.parse_comment(line) -> score.Comment

.. autofunction:: humdrum.parse_reference_record(line) -> score.Record

.. autofunction:: humdrum.parse_item

   >>> parse_item("=1", score)
   <__main__.Bar object at 0x7f982d7e6910>

   >>> parse_item("**kern", score)
   <__main__.Exclusive object at 0x7f982d793f10>

   >>> parse_item("*ICvox", score)
   <__main__.Tandem object at 0x7f982d7be3d0>

   >>> parse_item(".", score)
   <__main__.NullToken object at 0x7f982d7be4d0>

   >>> parse_item("c", score)
   KernError: Can't parse an item without knowing the spine type.


.. autofunction:: humdrum.parse_bar
.. autofunction:: humdrum.parse_tandem
.. autofunction:: humdrum.parse_data

Spine paths
-----------

Parsing the kern representation
-------------------------------


