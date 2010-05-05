from fractions import Fraction
import music
import py


def test_string_to_code():
    assert music.string_to_code("c", "#", "base40") == 4
    assert music.string_to_code("b", "", "base12") == 11
    assert music.string_to_code("b", "-", "base12") == 10
    assert music.string_to_code("b", "#", "base12") == 0


def test_calculate_duration():
    assert music.calculate_duration(16, 0) == Fraction(1, 16)
    assert music.calculate_duration(16) == Fraction(1, 16)
    assert music.calculate_duration(4, 1) == Fraction(3, 8)
    assert music.calculate_duration(4, 2) == Fraction(7, 16)
    assert music.calculate_duration(12, 1) == Fraction(1, 8)
    assert music.calculate_duration(0, 0) == Fraction(2, 1)
    assert music.calculate_duration(0, 1) == Fraction(3, 1)
    assert music.calculate_duration(0, 2) == Fraction(7, 2)
    assert music.calculate_duration("breve", 0) == Fraction(2, 1)
    assert music.calculate_duration("brevis", 0) == Fraction(2, 1)
    assert music.calculate_duration("longa", 0) == Fraction(4, 1)
    assert music.calculate_duration("longa", 1) == Fraction(6, 1)
    assert music.calculate_duration("maxima", 0) == Fraction(8, 1)
    assert music.calculate_duration("maxima", 1) == Fraction(12, 1)
    py.test.raises(music.MusicError, music.calculate_duration, "foo", 0)


def test_notename_to_humdrum():
    assert music.notename_to_humdrum("Cbb", 1) == "CCC--"
    assert music.notename_to_humdrum("Cbb", 2) == "CC--"
    assert music.notename_to_humdrum("Cbb", 3) == "C--"
    assert music.notename_to_humdrum("Cbb", 4) == "c--"
    assert music.notename_to_humdrum("Cbb", 5) == "cc--"
    assert music.notename_to_humdrum("D##", 5) == "dd##"
    assert music.notename_to_humdrum("D##", 0) == "DDDD##"
    assert music.notename_to_humdrum("D##", 7) == "dddd##"


def test_notename_to_lily():
    assert music.notename_to_lily("Cbb", 1) == "ceses,,"
    assert music.notename_to_lily("Cbb", 2) == "ceses,"
    assert music.notename_to_lily("Cbb", 3) == "ceses"
    assert music.notename_to_lily("Cbb", 4) == "ceses'"
    assert music.notename_to_lily("Cbb", 5) == "ceses''"
    assert music.notename_to_lily("D##", 5) == "disis''"
    assert music.notename_to_lily("D##", 0) == "disis,,,"
    assert music.notename_to_lily("D##", 7) == "disis''''"
