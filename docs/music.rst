Music functions and operations
==============================

.. autofunction:: music.calculate_duration

   Although the use of the reciprocal of a note value in the
   codification is convenient (for instance, two c notes with duration
   values of 1/4 and 1/8 are represented as "4c" and "8c",
   respectively), it's difficult to represent durations such as the
   breve, longa, and maxima numerically [#]_. Humdrum uses 0 as the
   duration of a breve, so we need to check for that. This function
   also accepts the strings "breve", "brevis", "longa", and "maxima"
   as an argument for ``dur``.

   .. [#] Actually, we could just continue to use the reciprocal, so
      if a breve has a value of 2, it could be represented as 1/2 in
      the codification. But it's easy to confuse 1/2 (the reciprocal
      of the duration of a breve) with a half-note.

.. autofunction:: music.string_to_code

