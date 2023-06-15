x = ["1", 2, 3, "4", "error"]


def test_handle_results():
    errors: list[str] = []
    y = filter(lambda r: type(r) == int, x)
    assert list(y) == [2, 3]
