"""
Demonstrate autouse fixtures.
all of the fixtures used by tests were named by the tests (or used usefixtures for that one class example). 
However, you can use autouse=True to get a fixture to run all of the time. 
This works well for code you want to run at certain times, but tests don’t really depend on any system state or data from the fixture.
The autouse feature is good to have around. But it’s more of an exception than a rule. Opt for named fixtures unless you have a really great reason not to.

"""

import pytest
import time


@pytest.fixture(autouse=True, scope='session')
def footer_session_scope():
    """Report the time at the end of a session."""
    yield
    now = time.time()
    print('--')
    print('finished : {}'.format(time.strftime('%d %b %X', time.localtime(now))))
    print('-----------------')


@pytest.fixture(autouse=True)
def footer_function_scope():
    """Report test durations after each function."""
    start = time.time()
    yield
    stop = time.time()
    delta = stop - start
    print('\ntest duration : {:0.3} seconds'.format(delta))


def test_1():
    """Simulate long-ish running test."""
    time.sleep(1)


def test_2():
    """Simulate slightly longer test."""
    time.sleep(1.23)

"""
The autouse feature is good to have around. But it’s more of an exception than a rule. 
Opt for named fixtures unless you have a really great reason not to.
"""