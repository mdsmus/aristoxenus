def sum_power(start, end):
    return reduce(operator.add, [pow(2, x) for x in range(start, end - 1, -1)])


def calculate_duration(durs, dots):
    # FIXME to work with fractions
    d = int("".join(durs))
    duration = Fraction(1, 2) if d == 0 else d
    max = math.floor(math.log(duration, 2)) * -1
    min = max - len(dots)
    return sum_power(min, max)


def string_to_code(note_name, code):
    base40 = [None,
              "cbb", "cb", "c", "c#", "c##", None,
              "dbb", "db", "d", "d#", "d##", None,
              "ebb", "eb", "e", "e#", "e##",
              "fbb", "fb", "f", "f#", "f##", None,
              "gbb", "gb", "g", "g#", "g##", None,
              "abb", "ab", "a", "a#", "a##", None,
              "bbb", "bb", "b", "b#", "b##"]

    dic = {'base40': base40}

    return dic[code].index(note_name)
