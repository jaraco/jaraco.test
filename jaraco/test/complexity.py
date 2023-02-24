import timeit
import statistics
import itertools


powers_of_two = (2**n for n in itertools.count())


def identity(x):
    return x


def is_linear_time(
    func, factory=identity, sizes=tuple(itertools.islice(powers_of_two, 10)), **ns
):
    """
    Does func run in linear time?

    >>> is_linear_time(lambda n: [str(val) for val in range(1,n+1)])
    True

    >>> def n_sq(n):
    ...     return [str(x*y) for x, y in itertools.product(range(n), range(n))]
    >>> is_linear_time(n_sq)
    False
    """

    stmt = 'func(data)'
    setup = 'data = factory(size)'
    # calculate time/size for each size
    norm_times = [
        timeit.timeit(
            stmt,
            setup,
            number=1,
            globals=dict(ns, func=func, factory=factory, size=size),
        )
        / size
        for size in sizes
    ]
    # the func was linear if norm_times is essentially constant
    ratio = statistics.stdev(norm_times) / norm_times[0]
    return ratio < 1
