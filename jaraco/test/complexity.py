import timeit
import itertools

import numpy


def is_linear(x, y):
    """Return True if the dataset is linear, False otherwise."""
    x = numpy.array(x)
    y = numpy.array(y)
    A = numpy.vstack([x, numpy.ones(len(x))]).T
    # Compute the slope and intercept of the regression line.
    slope, intercept = numpy.linalg.lstsq(A, y, rcond=None)[0]
    # Compute the residual sum of squares.
    residual_sum_of_squares = numpy.sum((y - (slope * x + intercept)) ** 2)
    # Compute the expected residual sum of squares for a linear
    # dataset.
    expected_residual_sum_of_squares = numpy.sum((y - y.mean()) ** 2)
    # Return True if the residual sum of squares is significantly less
    # than the expected residual sum of squares.
    return residual_sum_of_squares < expected_residual_sum_of_squares * 0.05


powers_of_two = (2**n for n in itertools.count())


def identity(x):
    return x


def is_linear_time(*args, **kwargs):
    """
    Does func run in linear time?

    >>> is_linear_time(lambda n: [str(val) for val in range(1,n+1)])
    True

    >>> def n_sq(n):
    ...     return [str(x*y) for x, y in itertools.product(range(n), range(n))]
    >>> is_linear_time(n_sq)
    False
    """
    return is_linear(*run_experiments(*args, **kwargs))


def run_experiments(
    func, factory=identity, sizes=tuple(itertools.islice(powers_of_two, 10)), **ns
):
    stmt = 'func(data)'
    setup = 'data = factory(size)'
    # time the experiments
    times = [
        timeit.timeit(
            stmt,
            setup,
            number=1,
            globals=dict(ns, func=func, factory=factory, size=size),
        )
        for size in sizes
    ]
    return sizes, times
