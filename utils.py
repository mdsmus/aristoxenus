import re


def isPython3():
    return sys.version[:1] == '3'


def isMatch(reg, string):
    tmp = re.search(reg, string)
    if tmp:
        return tmp.group()


def prev_string(string, i):
    previous = i - 1
    return '' if previous < 0 else string[previous]
