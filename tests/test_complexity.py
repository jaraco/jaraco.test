import itertools

from jaraco.test import complexity


def test_is_linear_time():
    def linear_func(n):
        return [str(val) for val in range(1, n + 1)]

    assert complexity.is_linear_time(linear_func)


def test_n_sq_is_not_linear_time():
    def n_sq(n):
        return [str(x * y) for x, y in itertools.product(range(n), range(n))]

    assert not complexity.is_linear_time(n_sq)
