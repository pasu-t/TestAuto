import pytest
from flaky import flaky
import random

"""
By default, flaky will retry a failing test once, but that behavior can be
overridden by passing values to the flaky decorator. It accepts two
parameters: max_runs, and min_passes; flaky will run tests up to max_runs
times, until it has succeeded min_passes times. Once a test passes min_passes
times, it’s considered a success; once it has been run max_runs times without
passing min_passes times, it’s considered a failure.
"""

flaky = flaky(max_runs=5, min_passes=1)

@flaky
@pytest.mark.parametrize('i', range(10))
def test_flaky_1(i):
    assert random.randint(1,10) >= 5

#conditional decorator

def conditional_decorator(dec, condition):
    def decorator(func):
        if not condition:
            # Return the function unchanged, not decorated.
            return func
        return dec(func)
    return decorator

@conditional_decorator(flaky, True)
@pytest.mark.parametrize('i', range(10))
def test_flaky_2(i):
    assert random.randint(1,10) >= 5


# pytest -v -s --tb=no test_flaky.py::test_flaky_1
