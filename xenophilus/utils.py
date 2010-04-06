import re


def isPython3():
    return sys.version[:1] == '3'


def search_string(pattern, string):
    """Like re.search but return the string that matches the pattern
    instead of a Match object.
    """

    tmp = re.search(pattern, string)
    if tmp:
        return tmp.group()


def prev_string(string, i):
    previous = i - 1
    return '' if previous < 0 else string[previous]
