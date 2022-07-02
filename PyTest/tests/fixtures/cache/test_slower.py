import datetime
import pytest
import random
import time

"""
The fixture is autouse, so it doesn’t need to be referenced from the test. The
request object is used to grab the nodeid for use in the key. The nodeid is a
unique identifier that works even with parametrized tests. We prepend the key
with ’duration/’ to be good cache citizens. The code above yield runs before
the test function; the code after yield happens after the test function.
"""

@pytest.fixture(autouse=True)
def check_duration(request, cache):
    key = 'duration/' + request.node.nodeid.replace(':', '_')
    # nodeid's can have colons
    # keys become filenames within .cache
    # replace colons with something filename safe
    start_time = datetime.datetime.now()
    yield
    stop_time = datetime.datetime.now()
    this_duration = (stop_time - start_time).total_seconds()
    last_duration = cache.get(key, None)
    cache.set(key, this_duration)
    if last_duration is not None:
        errorstring = "test duration over 2x last duration"
        print(this_duration,last_duration)
        assert this_duration <= last_duration * 2, errorstring


@pytest.mark.parametrize('i', range(5))
def test_slow_stuff(i):
    time.sleep(random.random())

# pytest --cache-clear test_slower.py
# pytest -q --tb=line test_slower.py
# pytest -q --cache-show
