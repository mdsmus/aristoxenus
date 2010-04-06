import re
import sys


def ispython3():
    """Return True if the main version of python is 3"""
    
    return sys.version[:1] == '3'


def search_string(pattern, string):
    """Like re.search but return the string that matches the pattern
    instead of a Match object."""

    tmp = re.search(pattern, string)
    if tmp:
        return tmp.group()
