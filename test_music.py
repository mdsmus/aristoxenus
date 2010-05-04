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
