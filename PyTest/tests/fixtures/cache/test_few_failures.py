"""Demonstrate -lf and -ff with failing tests."""

import pytest
from pytest import approx

"""
Maybe you can spot the problem right off the bat. But let’s pretend the test
is longer and more complicated, and it’s not obvious what’s wrong. Let’s run
the test again to see the failure again. You can specify the test case on the
command line:
# pytest --verbose --tb=no --lf test_pass_fail.py
# pytest --verbose --tb=no --ff test_pass_fail.py
# pytest -q "test_few_failures.py::test_a[1e+25-1e+23-1.1e+25]"
"""

testdata = [
    # x, y, expected
    (1.01, 2.01, 3.02),
    (1e25, 1e23, 1.1e25),
    (1.23, 3.21, 4.44),
    (0.1, 0.2, 0.3),
    (1e25, 1e24, 1.1e25)
]


@pytest.mark.parametrize("x,y,expected", testdata)
def test_a(x, y, expected):
    """Demo approx()."""
    sum_ = x + y
    assert sum_ == approx(expected)

"""
If you don’t want to copy/paste or there are multiple failed cases you’d like
to rerun, --lf is much easier. And if you’re really debugging a test failure,
another flag that might make things easier is --showlocals, or -l for short:
$ pytest -q --lf -l test_few_failures.py
You can see the stored information with --cache-show:
# pytest --cache-show
"""