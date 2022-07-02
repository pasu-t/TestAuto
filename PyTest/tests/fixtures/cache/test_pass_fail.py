def test_this_passes():
    assert 1 == 1


def test_this_fails():
    assert 1 == 2

# pytest --verbose --tb=no --lf test_pass_fail.py
# pytest --verbose --tb=no --ff test_pass_fail.py