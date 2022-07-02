import pytest
import datetime
import random
import time
from collections import namedtuple

Duration = namedtuple('Duration', ['current', 'last'])

"""
You can easily see the duration data separate from the cache data due to the
prefixing of cache data names. However, it’s interesting that the lastfailed
functionality is able to operate with one cache entry. Our duration data is
taking up one cache entry per test. Let’s follow the lead of lastfailed and
fit our data into one entry.

We are reading and writing to the cache for every test. We could split up the
fixture into a function scope fixture to measure durations and a session
scope fixture to read and write to the cache. However, if we do this, we
can’t use the cache fixture because it has function scope. Fortunately, a
quick peek at the implementation on GitHub[9] reveals that the cache fixture
is simply returning request.config.cache. This is available in any scope 

The duration_cache fixture is session scope. It reads the previous entry or an
empty dictionary if there is no previous cached data, before any tests are
run. In the previous code, we saved both the retrieved dictionary and an
empty one in a namedtuple called Duration with accessors current and last. We
then passed that namedtuple to the check_duration fixture, which is function
scope and runs for every test function. As the test runs, the same namedtuple
is passed to each test, and the times for the current test runs are stored in
the d.current dictionary. At the end of the test session, the collected
current dictionary is saved in the cache.
"""

@pytest.fixture(scope='session')
def duration_cache(request):
    key = 'duration/testdurations'
    d = Duration({}, request.config.cache.get(key, {}))
    yield d
    request.config.cache.set(key, d.current)


@pytest.fixture(autouse=True)
def check_duration(request, duration_cache):
    d = duration_cache
    nodeid = request.node.nodeid
    start_time = datetime.datetime.now()
    yield
    duration = (datetime.datetime.now() - start_time).total_seconds()
    d.current[nodeid] = duration
    if d.last.get(nodeid, None) is not None:
        errorstring = "test duration over 2x last duration"
        assert duration <= (d.last[nodeid] * 2), errorstring


@pytest.mark.parametrize('i', range(5))
def test_slow_stuff(i):
    time.sleep(random.random())

# pytest -q --cache-clear test_slower_2.py
# pytest -q --tb=no test_slower_2.py
# pytest -q --chache-show

