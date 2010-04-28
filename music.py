def sum_power(start, end):
    return reduce(operator.add, [pow(2, x) for x in range(start, end - 1, -1)])


def calculate_duration(durs, dots):
    # FIXME to work with fractions
    d = int("".join(durs))
    duration = Fraction(1, 2) if d == 0 else d
    max = math.floor(math.log(duration, 2)) * -1
    min = max - len(dots)
    return sum_power(min, max)


def string_to_code(notename, acc, code):
    """
    >>> string_to_code('b', '#', 'base12')
    0
    """
    
    notes = "c d e f g a b".split()
    dic = {'base40': ([3, 9, 15, 20, 26, 32, 38], 40),
           'base12': ([0, 2, 4, 5, 7, 8, 11], 12)}

    code_list = dic[code][0]
    n = code_list[notes.index(notename.lower())]
    if acc:
        op = 1 if acc[0] == "#" else -1
    else:
        op = 0
    return  (n + (len(acc) * op)) % dic[code][1]
