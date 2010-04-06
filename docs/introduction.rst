Introduction
============

Aristoxenus is a python library to process and generate music
information. It has a data structure for musical scores, a parser for
the humdrum format, functions to operate on musical data, and
functions to export to formats such as abc.

The Score class
===============

The basic data structure in the aristoxenus library is the class
`Score`. It's modeled after the humdrum format and uses similar
terminology such as spines and interpretations. But this data
structure can be used independently of the humdrum format. Also, other
formats such as abc and lilypond can be parsed into the `Score` data
structure.

The class taxonomy for the `Score` data structure can be seen in
figure
