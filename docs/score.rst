The Score data structure
========================

The basic data structure in the aristoxenus library is the class
:class:`Score`. It's modeled after the humdrum format and uses similar
terminology such as spines and interpretations. But this data
structure can be used independently of the humdrum format. Also, other
formats such as abc and lilypond can be parsed into the :class:`Score`
data structure.

We can see the class taxonomy for the Score data structure in the
following diagram:

.. image:: figs/classes.png
   :width:  550
   :height: 487

The Score class
---------------

.. class:: score.Score()

The class :class:`score.Score` is a subclass of :class:`list`. Every line of
a humdrum file is parsed and the result is stored as an item of
:class:`Score`. So, if we have ``s = Score()``, ``s[2]`` will return
the third line of a parsed humdrum file. For instance, the result of
``parse_string("**kern\n4c\n\n4d\n*-")`` will be something like::

  [[<score.Exclusive object at 0x7f982d7a9590>],
   [<score.Note object at 0x7f982d715690>],
   [<score.Note object at 0x7f982d715650>],
   [<score.Tandem object at 0x7f982d715350>]]


.. attribute:: Score.title
               Score.composer

The attributes :attr:`Score.title` and :attr:`Score.composer` are
copied from reference records to allow easy and quick access to this
information (useful when generation data for notation programs).

.. attribute:: Score.filename 

name of the original humdrum file

.. attribute:: Score.spine_number

the number of original spines

.. attribute:: Score.spine_types

list of strings with the original types of spines (for instance,
``["kern", "dynam"]``).


The Note class
--------------


.. class:: score.Note()


.. attribute:: name

  A string with the note name in English such as "Ab" and "C##".

.. attribute:: duration

  A fractional number indicating the duration.

.. attribute:: octave

  An integer, where 4 is the central octave.

.. attribute:: articulations

  A list of strings denoting an articulation such as "harmonic" and "turn".

.. attribute:: beams

  A list of keywords denoting beam commands.

.. attribute:: code

  Numeric code for the note name. For instance, if the
  :attr:`Note.name` is "Ab" the value for :attr:`Note.code` should be
  8 if :attr:`system` is "et12" and 31 if :attr:`system` is "base40".

.. attribute:: system

  The numeric system used to parse the note. Values can be "et12",
  "base40", "base96" and so on.


The idea to have a code number in the :class:`Note` class is to
provide some optimization. (i.e. the code number doesn't have to be
calculated after the file is parsed). It's probably not a good idea to
modify the :attr:`Note.code` and :attr:`Note.system` attributes after
the file has been parsed.


The Tandem class
----------------


.. class:: score.Tandem

The tandem class stores the kind of tandem interpretation as a string
in :attr:`Score.type` and the actual value in :attr:`Score.data`. The
following table shows each value :attr:`type` can have and the type
of :attr:`data`, with a brief example:

+-----------------+----------------------------+------------------------+
| keyword         | type of Note.data          | example                |
+=================+============================+========================+
| "clef"          | string                     | "treble"               |
+-----------------+----------------------------+------------------------+
| "instr-class"   | string                     | "vox"                  |
+-----------------+----------------------------+------------------------+
| "instr-group"   | string                     | "ripn"                 |
+-----------------+----------------------------+------------------------+
| "instrument"    | string                     | "bass"                 |
+-----------------+----------------------------+------------------------+
| "key-signature" | integer or list of strings | 2 or ``["f#", "cb"]``  |
+-----------------+----------------------------+------------------------+
| "tempo"         | number                     | 88.8                   |
+-----------------+----------------------------+------------------------+
| "meter"         | string                     | "12/8" [#f1]_          |
+-----------------+----------------------------+------------------------+
| "timebase"      | number                     | 12                     |
+-----------------+----------------------------+------------------------+
| "transposing"   | string                     | "d1c2"                 |
+-----------------+----------------------------+------------------------+
| "key"           | string                     | "Ab"                   |
+-----------------+----------------------------+------------------------+

If the key signature is one of the standard used in western tonal
music, a positive integer is used to indicate the number of sharps and
a negative integer to indicate the number of flats. If the key
signature is not standard (e.g. it has "Bb" and "F#") the notes are
saved in a list.

The instrument names follow the abbreviations in the Appendix II of
the humdrum manual. (See also :ref:`todo`).

.. rubric:: Footnotes

.. [#f1] It can't be a rational because tempos like 4/4 will be normalized to 1/1.


The Record class
----------------


.. class:: score.Record

Reference records are partially parsed and saved in the
:class:`Record` class. The reference codes are saved in
:attr:`Record.name` as a string (for example, "OTL@@FUR" and "OTL")
while the reference data is saved in :attr:`Record.data` (for example,
"Ai preit la biele stele"). The parser doesn't further process the
data in :attr:`Record.name`. The only exception is the reference code
for the title and composer, which are saved in the slots with the same
name in the :class:`Record` class. See section :ref:`todo` for things
that need to be done.
