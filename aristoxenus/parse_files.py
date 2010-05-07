#!/usr/bin/python

import os
import humdrum


wtc1 = 'data/wtc-1/'
wtc2 = 'data/wtc-2/'

def parse_collection(directory):
    for f in os.listdir(directory):
        try:
            print ".",
            humdrum.parse_file(directory + f)
        except IndexError:
            print "\n[NOT]", f


parse_collection(wtc1)
parse_collection(wtc2)
