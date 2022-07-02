import warnings
import pytest


def lame_function():
    warnings.warn("Please stop using this", DeprecationWarning)
    # rest of function


def test_lame_function(recwarn):
    lame_function()
    assert len(recwarn) == 1
    w = recwarn.pop()
    assert w.category == DeprecationWarning
    assert str(w.message) == 'Please stop using this'

"""
The recwarn value acts like a list of warnings, and each warning in the list
has a category, message, filename, and lineno defined, as shown in the code.

The warnings are collected at the beginning of the test. If that is
inconvenient because the portion of the test where you care about warnings is
near the end, you can use recwarn.clear() to clear out the list before the
chunk of the test where you do care about collecting warnings.

In addition to recwarn, pytest can check for warnings with pytest.warns():
"""

def test_lame_function_2():
    with pytest.warns(None) as warning_list:
        lame_function()

    assert len(warning_list) == 1
    w = warning_list.pop()
    assert w.category == DeprecationWarning
    assert str(w.message) == 'Please stop using this'

"""
The pytest.warns() context manager provides an elegant way to demark what
portion of the code you’re checking warnings. The recwarn fixture and the
pytest.warns() context manager provide similar functionality, though, so the
decision of which to use is purely a matter of taste.
"""
