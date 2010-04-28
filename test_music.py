import music


def test_string_to_code():
    assert music.string_to_code("c", "#", "base40") == 4
    assert music.string_to_code("b", "", "base12") == 11
    assert music.string_to_code("b", "-", "base12") == 10
    assert music.string_to_code("b", "#", "base12") == 0
