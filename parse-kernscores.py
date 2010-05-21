#!/usr/bin/env python

from __future__ import print_function

import os.path

from aristoxenus import parse
from aristoxenus import emit
from aristoxenus import music

kernscoredir = "/home/kroger/Documents/kernscores"

error_files = 0

with open(os.path.join(kernscoredir, "filelist")) as filelist:
    for line in filelist:
        filename = os.path.join(kernscoredir, line.strip('\n'))
        try:
            parse.humdrum.parse_file(filename)
        except (IndexError, ValueError, KeyError, parse.humdrum.kern.KernError, parse.humdrum.main.HumdrumError):
            print("[ERROR]", filename)
            error_files += 1

print("{0} errors".format(error_files))

