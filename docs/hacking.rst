Helping with Aristoxenus' development
=====================================

Configuring Emacs
-----------------

Put the following the file .dir-locals.el:

        ((nil . ((default-directory . "~/Documents/aristoxenus/")
                 (py-master-file . "test-interactive.py"))))


.. _todo:

Things to do
------------

These are things that need to be done eventually but are not top
priority for 1.0 (but they may be important for converting to notation
formats such as lilypond).

process reference records

  It may be a good idea to save reference records in a more
  descriptive names.

parse all barline elements

  We don't parse signs for barline visual rendering. It's a mostly
  easy job, but we need to think of a useful internal representation
  for those things. See the `humdrum documentation
  <http://humdrum.org/Humdrum/representations/kern.html#Barlines>`_.


  The file ``all-bars.txt`` has a list of all bar types used in the
  40,000+ kernscores files. This list is a good reference for
  real-life testing.

consider if we should use more descriptive names for instruments

  The names used by default are not very descriptive, like "Ibspro"
  for "basso profondo". Is it a good thing to use names like
  "basso-profondo"?
