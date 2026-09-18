def func(x):
    return x + 1

class TestClass:
    def test1(self):
        assert func(4) == 5

    def test2(self):
        assert func(-1) == 0
