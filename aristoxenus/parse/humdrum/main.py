from __future__ import print_function
from __future__ import division
from itertools import count
import re
import sys

from aristoxenus import utils
from aristoxenus import music
from aristoxenus import score
from aristoxenus.parse.humdrum import kern

debug = False


class HumdrumError(Exception):
    """Exception class for humdrum data."""
    pass


def humdrum_error(message):
    """Helper function to raise parsing errors."""

    raise HumdrumError(message)


## parse elements


def parse_spine_path(item):
    d = {'*-': "spine-end",
         '*+': "spine-add",
         '*^': "spine-split",
         '*v': "spine-join",
         '*x': "spine-swap"}

    return score.SpinePath(d[item])


def parse_bar(item):
    """Search a string for bar elements and return a :class:`score.Bar`

    This function will search for the bar number, if a bar begins or
    ends a repetition and if it's a double bar. Humdrum has a bunch of
    syntax for visual bar lines that we don't parse. See :ref:`todo`.
    """

    return score.Bar(utils.search_string("[0-9]+([a-z]+)?", item),
                     bool(utils.search_string(":\\||:!", item)),
                     bool(utils.search_string("\\|:|!:", item)),
                     bool(utils.search_string("==", item)))


def parse_clef(item):
    dic = {"F4": "bass",
           "G2": "treble",
           "C3": "alto",
           "C4": "tenor",
           "Gv2": "tenor8",
           "C1": "soprano",
           "C2": "mezzo",
           "X" : "perc",
           # we have these as defaults
           "C" : "alto",
           "F" : "bass",
           "G" : "treble"}

    return score.Tandem("clef", dic[item])


def parse_expansion_list(item):
    return score.Tandem("expansion-list", item[:-1].split(','))


def parse_key_signature(item):
    item = item[1:-1]
    split_item = [item[i] + item[i+1] for i in range(0, len(item), 2)]
    list_keys = [utils.replace_flats(x.lower().strip()) for x in split_item]
    size = len(list_keys)
    sharps = music.accidentals_table[size]
    flats = music.accidentals_table[-size]

    if list_keys == sharps:
        return score.Tandem("key-signature", size)
    elif list_keys == flats:
        return score.Tandem("key-signature", -size)
    else:
        return score.Tandem("key-signature", list_keys)


def parse_key(item):
    return score.Tandem("key", utils.replace_flats(item))


def parse_tandem(item):
    if item.startswith("*clef"):
        return parse_clef(item[5:])
    elif item.startswith("*IC"):
        return score.Tandem("instr-class", item[3:])
    elif item.startswith("*IG"):
        return score.Tandem("instr-group", item[3:])
    elif item.startswith("*ITr"):
        return score.Tandem("transposing", item[4:])
    elif item.startswith("*I:"):
        return score.Tandem("instrument-user", item[3:])
    elif item.startswith("*I"):
        return score.Tandem("instrument", item[2:])
    elif item.startswith("*k"):
        return parse_key_signature(item[2:])
    elif item.startswith("*MM"):
        return score.Tandem("tempo", float(item[3:]))
    elif item.startswith("*M"):
        return score.Tandem("meter", item[2:])
    elif item.startswith("*tb"):
        return score.Tandem("timebase", float(item[3:]))
    elif item.startswith("*>["):
        return parse_expansion_list(item[3:])
    elif item.startswith("*>"):
        return score.Tandem("label", item[2:])
    elif item.endswith(":"):
        return parse_key(item[1:-1])
    else:
        return score.Tandem(None, item[1:])


def parse_data(data_type, item, note_system="base40", lineno=1, itemno=1):
    """Apply the right function to parse ``data_type``.

    For instance, if ``data_type`` is 'kern', then ``parse_data`` will
    apply ``parse_kern`` to the rest of arguments. ``parse_data`` has
    a dispatch table to match the data type to the function. When the
    parser for a new humdrum data type is implemented, the dispatch
    table need to be updated. If an unknown type is found the item
    will be returned without any parsing.
    """

    def unknown_type(item, note_system, lineno=1, itemno=1):
        return score.UnknownType(item)

    dispatch = {"kern": kern.parse_kern}

    return dispatch.get(data_type, unknown_type)(item, note_system, lineno, itemno)


## basic parser


def parse_item(item, sco, note_system="base40", lineno=1, itemno=1):
    """Parse each item of a humdrum spine.

    We can parse general items like :class:`score.Bar`,
    :class:`score.score.Exclusive`, :class:`score.Tandem`,
    :class:`score.score.Comment`, and :class:`score.NullToken` without
    previous information since the type of data is defined in the
    string itself (e.g. the '**' in '**kern' defines it as an
    exclusive interpretation). However, we can't parse other data
    records without knowing their spine type. When an exclusive
    interpretation is found the spine type is appended to
    :attr:`Score.spine_types`. This attribute can be used to know the
    spine type of an item.
    """

    if type(item) is list:
        return [parse_item(i, sco, note_system, lineno, itemno) for i in item]
    elif item.startswith("="):
        return parse_bar(item)
    elif item == "*":
        return score.NullInterpretation()
    elif item.startswith("**"):
        spine_type = item[2:]
        sco.spine_types.append(spine_type)
        return score.Exclusive(spine_type)
    elif item in ["*-", "*+", "*^", "*v", "*x"]:
        return parse_spine_path(item)
    elif item.startswith("*"):
        if item.startswith("*I:"):
            sco.spine_names.append(item[3:])
        elif item.startswith("*I") and not item.startswith("*IC"):
            # what is the logic in this code again?
            # and len(sco.spine_names) != itemno - 1
            sco.spine_names.append(item[2:])

        return parse_tandem(item)
    elif item.startswith("!"):
        return parse_comment(item)
    elif item == ".":
        return score.NullToken()
    else:
        spine_type_list = sco.spine_types
        if len(spine_type_list) == 0:
            humdrum_error("Can't parse an item without knowing the spine type.")
        else:
            if itemno > len(sco.spine_types) - 1:
                humdrum_error("Item index is greater than number of"
                              " spines on line {0}".format(lineno))
            data_type = sco.spine_types[itemno]
        return parse_data(data_type, item, note_system, lineno, itemno)


def parse_reference_record(line):
    """Separate the data in the Reference from the ! character.

    Since a reference record must start with 3 exclamation marks we
    don't need to use regular expressions to separate the actual
    comment from the comment character. We split the line by the first
    occurrence of ':' in order to prevent splitting a colon inside the
    text, such as '!!!OTL: Title: more stuff'.
    """

    s = line.split(":", 1)
    return score.Record(s[0][3:].strip(), s[1].strip())


def parse_comment(line):
    """Separate the actual comment from the comment character."""

    match = re.match("^(!+)(.*)$", line)
    return score.Comment(match.group(2).strip(), len(match.group(1)))


def split_spine(line, sco, lineno=1):
    sline = line.split("\t")

    if sco.split_spine:
        for n in sco.split_spine:
            sline[n:n+2] = [sline[n:n+2]]

    if "*^" in sline:
        sco.split_spine += [num for num, item in enumerate(sline) if item == "*^"]

    # FIXME: numbers not right, run ./humdiff data/split-spine-8.krn
    # with next line uncommented
    # TODO: make unit-tests for split-spine
    print(sline, sco.split_spine, lineno)

    for n, i in enumerate(sline):
        if "*v" in i and sco.split_spine:
            sco.split_spine.remove(n)

    return sline


def parse_line(line, sco, note_system="base40", lineno=1):
    """Parse a line, append the parsed result into the sco and return the sco

    A line can be a BlankLine, a reference record, a comment, or have
    tabular data (spines) in which case we parse each item
    individually with :func:`humdrum.parse_item`. Both reference
    record and comments start with !, but a reference record starts
    with 3 exclamation marks (!!!) while a comment starts with one,
    two, four or more exclamation marks. Global comments have more
    than one exclamation marks and will be catched by this function.
    Local comments have only one exclamation mark and are applied to an
    individual spine. A local comment will be catched in
    :func:`humdrum.parse_item()`.
    """

    if utils.search_string(r"^[ \t]*$", line) is not None:
        sco.append(score.BlankLine())
    elif utils.search_string(r"^!{3}[a-zA-Z ]+", line):
        record = parse_reference_record(line)
        if record.name.startswith("COM"):
            sco.composer = record.data
        elif record.name.startswith("OTL"):
            sco.title = record.data

        sco.append(record)
    elif utils.search_string(r"^(!{2})|(!{4,})[a-zA-Z ]+", line):
        sco.append(parse_comment(line))
    else:
        sline = enumerate(split_spine(line, sco, lineno))
        parsed = [parse_item(i, sco, note_system, lineno, n) for n, i in sline]
        sco.append(parsed)
    return sco


def parse_string(string, note_system="base40"):
    """Parse a string with humdrum data  and return a :class:`score.Score`.

    This function is useful mainly for tests and to parse data
    directly from user input. To parse large quantities of data you
    should use :func:`parse_file()` instead.
    """

    s = score.Score()
    for line, lineno in zip(string.split('\n'), count(1)):
        parse_line(line, s, note_system, lineno)
    return s


def parse_file(filename, note_system="base40"):
    """Parse a humdrum file and return a :class:`score.Score`."""

    with open(filename) as f:
        s = score.Score()
        for line, lineno in zip(f, count(1)):
            parse_line(line.rstrip(), s, note_system, lineno)
        return s
