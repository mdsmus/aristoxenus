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

The following attributes are used by :func:`humdrum.kern_tokenizer`.
The shouldn't be accessed by other functions or directly.

.. attribute:: humdrum.types

   A dictionary that maps a data record type such as duration,
   articulation, or beam to che characters that compose those types
   and an error message. The format is ``<type>: (<characteres>,
   <error message>)``, for example::

   'dur': ("0123456789", "Duration must be together."),
   'note': ("abcdefgABCDEFG", "Notes must be together."),

.. attribute:: humdrum.beams

   A dictionary that maps humdrum code for beams to full names, for
   example::

   'L': 'beam-start',
   'J': 'beam-end',

.. attribute:: humdrum.art

   A dictionary that maps humdrum code for articulations to full
   names, for example::

   '$': "inverted-turn",
   'R': "end-with-turn",
   'u': "down-bow",

.. autofunction:: humdrum.parse_kern

   Main function to parse kern data. If the input is a multiple stop
   (notes separated by spaces in humdrum) it will return a
   :class:`score.MultipleStop` object with notes and rests inside. If
   not, it'll return either a note or a rest. (The other kern elements
   such as null tokens and local comments are handled by
   :func:`humdrum.parse_item`). Most of the parsing is actually done
   by :func:`humdrum.parse_kern_item` and
   :func:`humdrum.kern_tokenizer`. Here's an example (the resulting
   type is a MultipleStop, and not a list):

   >>> parse_kern("c4 d4")
   [<__main__.Note object at 0x24fb510>, <__main__.Note object at 0x24fb050>]

.. autofunction:: humdrum.kern_tokenizer

   Breaks a kern data record in elements and returns a dictionary
   where the keyword is the type of element and the value is the
   element itself in a list. We put the elements in a list to make it
   easier to append and count elements.

   >>> kern_tokenizer("CC4;/")
   {'note': ['C', 'C'], 'dur': ['4'], 'art': ['fermata', 'up-stem']})


   The tokenizer reads one charater at a time in the string, comparing
   the current character (``c``) with the previous (``p``). A big
   conditional expression checks (using the subfunction ``_is``) if
   the current character is of a certain type such as duration, note,
   or rest and append the character (or a more mnemonic representation
   of it, in the case of articulations) to the ``tokens`` dictionary.
   Here's an snippet of the conditional::

    if _is(c, 'dur'):
        parse(c, 'dur', (not p or not tokens['dur'] or _is(p, 'dur')))

   The ``parse`` subfunction appends the character to the ``tokens``
   dictionary or raises a :class:`humdrum.KernError` if the condition
   is not met. In the example above, the condition is that the
   previous character must be either a duration or nothing (that is,
   the current character is the first of the string) and it shouldn't
   have a duration that was parsed before in the string. This avoids
   the case of having repeated duration such as "4cc4".

   The code looks uglish, but it's way faster than using pyparsing and
   has way less dependencies than using ply. It may be a good idea to
   generalize the tokenizer using ply or a state machine if more
   parsing like this will be done for other spine types.

.. autofunction:: humdrum.parse_kern_item

   Takes the output from :func:`humdrum.kern_tokenizer` and process it
   further; checking for common mistakes such as having a note without
   a duration or having a note and a rest at the same time. This
   function will also create and return :class:`score.Note` and
   :class:`score.Rest` objects. It'll call functions such as
   :func:`humdrum.parse_kern_octave`, :func:`humdrum.parse_kern_note`,
   and :func:`music.string_to_code` to do the dirty work.

   >>> parse_kern_item("c4")
   <__main__.Note object at 0x252aed0>


.. autofunction:: humdrum.parse_kern_octave
.. autofunction:: humdrum.parse_kern_note


The following signifiers are not implemented yet:

#. appoggiatura (P p)
#. acciacatura (q)
#. phrase elision (&)
#. editorial marks (x X y Y ?)

Generic ornaments (O) and a generic articulations (I) will never be
implemented because what's the point in having those? They are
silently ignored by the parser.
