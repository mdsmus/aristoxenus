from fractions import Fraction
from aristoxenus import music
import py

# power_two_series

def test_power_two_series_1():
    assert music.power_two_series(1) == [1]

def test_power_two_series_3():
    assert music.power_two_series(3) == [1, 2]

def test_power_two_series_7():
    assert music.power_two_series(7) == [1, 2, 4]

def test_power_two_series_15():
    assert music.power_two_series(15) == [1, 2, 4, 8]


# string_to_code

def test_string_to_code_cs_base40():
    assert music.string_to_code("c", "#", "base40") == 4

def test_string_to_code_b_base12():
    assert music.string_to_code("b", "", "base12") == 11

def test_string_to_code_bf_base12():
    assert music.string_to_code("b", "-", "base12") == 10

def test_string_to_code_bs_base12():
    assert music.string_to_code("b", "#", "base12") == 0


# calculate_duration

def test_calculate_duration_16_0():
    assert music.calculate_duration(16, 0) == Fraction(1, 16)

def test_calculate_duration_16():
    assert music.calculate_duration(16) == Fraction(1, 16)

def test_calculate_duration_4_1():
    assert music.calculate_duration(4, 1) == Fraction(3, 8)

def test_calculate_duration_4_2():
    assert music.calculate_duration(4, 2) == Fraction(7, 16)

def test_calculate_duration_12_1():
    assert music.calculate_duration(12, 1) == Fraction(1, 8)

def test_calculate_duration_0_0():
    assert music.calculate_duration(0, 0) == Fraction(2, 1)

def test_calculate_duration_0_1():
    assert music.calculate_duration(0, 1) == Fraction(3, 1)

def test_calculate_duration_0_2():
    assert music.calculate_duration(0, 2) == Fraction(7, 2)

def test_calculate_duration_breve():
    assert music.calculate_duration("breve", 0) == Fraction(2, 1)

def test_calculate_duration_brevis():
    assert music.calculate_duration("brevis", 0) == Fraction(2, 1)

def test_calculate_duration_longa_0():
    assert music.calculate_duration("longa", 0) == Fraction(4, 1)

def test_calculate_duration_longa_1():
    assert music.calculate_duration("longa", 1) == Fraction(6, 1)

def test_calculate_duration_maxima_0():
    assert music.calculate_duration("maxima", 0) == Fraction(8, 1)

def test_calculate_duration_maxima_1():
    assert music.calculate_duration("maxima", 1) == Fraction(12, 1)

def test_calculate_duration_error_foo_as_duration():
    py.test.raises(music.MusicError, music.calculate_duration, "foo", 0)


# frac_to_dur

def test_frac_to_dur_2():
    assert music.frac_to_dur(2) == "0"

def test_frac_to_dur_3_8():
    assert music.frac_to_dur(Fraction(3, 8)) == "4."

def test_frac_to_dur_3_4():
    assert music.frac_to_dur(Fraction(3, 4)) == "2."

def test_frac_to_dur_7_8():
    assert music.frac_to_dur(Fraction(7, 8)) == "2.."

def test_frac_to_dur_7_16():
    assert music.frac_to_dur(Fraction(7, 16)) == "4.."

def test_frac_to_dur_error_13_4():
    py.test.raises(music.MusicError, music.frac_to_dur, Fraction(13, 4))


# notename_to_humdrum

def test_notename_to_humdrum_c2b1():
    assert music.notename_to_humdrum("Cbb", 1) == "CCC--"

def test_notename_to_humdrum_c2b2():
    assert music.notename_to_humdrum("Cbb", 2) == "CC--"

def test_notename_to_humdrum_c2b3():
    assert music.notename_to_humdrum("Cbb", 3) == "C--"

def test_notename_to_humdrum_c2b4():
    assert music.notename_to_humdrum("Cbb", 4) == "c--"

def test_notename_to_humdrum_c2b5():
    assert music.notename_to_humdrum("Cbb", 5) == "cc--"

def test_notename_to_humdrum_d2s5():
    assert music.notename_to_humdrum("D##", 5) == "dd##"

def test_notename_to_humdrum_d2s0():
    assert music.notename_to_humdrum("D##", 0) == "DDDD##"

def test_notename_to_humdrum_d2s7():
    assert music.notename_to_humdrum("D##", 7) == "dddd##"


# notename_to_lily

def test_notename_to_lily_c2f1():
    assert music.notename_to_lily("Cbb", 1) == "ceses,,"

def test_notename_to_lily_c2f2():
    assert music.notename_to_lily("Cbb", 2) == "ceses,"

def test_notename_to_lily_c2f3():
    assert music.notename_to_lily("Cbb", 3) == "ceses"

def test_notename_to_lily_c2f4():
    assert music.notename_to_lily("Cbb", 4) == "ceses'"

def test_notename_to_lily_c2f5():
    assert music.notename_to_lily("Cbb", 5) == "ceses''"

def test_notename_to_lily_d2s5():
    assert music.notename_to_lily("D##", 5) == "disis''"

def test_notename_to_lily_d2s0():
    assert music.notename_to_lily("D##", 0) == "disis,,,"

def test_notename_to_lily_d2s7():
    assert music.notename_to_lily("D##", 7) == "disis''''"
