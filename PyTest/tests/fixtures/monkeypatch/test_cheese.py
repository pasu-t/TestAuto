import copy
import cheese

"""
One problem with this is that anyone who runs this test code will overwrite
their own cheese preferences file. That’s not good.
"""
def test_def_prefs_full():
    cheese.write_default_cheese_preferences()
    expected = cheese._default_prefs
    actual = cheese.read_cheese_preferences()
    assert expected == actual

"""
If a user has HOME set, os.path.expanduser() replaces ~ with whatever is in a
user’s HOME environmental variable. Let’s create a temporary directory and
redirect HOME to point to that new temporary directory:
"""

def test_def_prefs_change_home(tmpdir, monkeypatch):
    monkeypatch.setenv('HOME', tmpdir.mkdir('home'))
    cheese.write_default_cheese_preferences()
    expected = cheese._default_prefs
    actual = cheese.read_cheese_preferences()
    assert expected == actual

"""
It is a pretty good test, but relying on HOME seems a little
operating-system dependent. And a peek into the documentation online for
expanduser() has some troubling information, including “On Windows, HOME and
USERPROFILE will be used if set, otherwise a combination of….”[10] Dang. That
may not be good for someone running the test on Windows. Maybe we should take
a different approach.

Instead of patching the HOME environmental variable, let’s patch expanduser:
"""
def test_def_prefs_change_expanduser(tmpdir, monkeypatch):
    fake_home_dir = tmpdir.mkdir('home')
    monkeypatch.setattr(cheese.os.path, 'expanduser',
                        (lambda x: x.replace('~', str(fake_home_dir))))
    cheese.write_default_cheese_preferences()
    expected = cheese._default_prefs
    actual = cheese.read_cheese_preferences()
    assert expected == actual


def test_def_prefs_change_defaults(tmpdir, monkeypatch):
    # write the file once
    fake_home_dir = tmpdir.mkdir('home')
    monkeypatch.setattr(cheese.os.path, 'expanduser',
                        (lambda x: x.replace('~', str(fake_home_dir))))
    cheese.write_default_cheese_preferences()
    defaults_before = copy.deepcopy(cheese._default_prefs)

    # change the defaults
    monkeypatch.setitem(cheese._default_prefs, 'slicing', ['provolone'])
    monkeypatch.setitem(cheese._default_prefs, 'spreadable', ['brie'])
    monkeypatch.setitem(cheese._default_prefs, 'salads', ['pepper jack'])
    defaults_modified = cheese._default_prefs

    # write it again with modified defaults
    cheese.write_default_cheese_preferences()

    # read, and check
    actual = cheese.read_cheese_preferences()
    assert defaults_modified == actual
    assert defaults_modified != defaults_before

"""
The del forms are pretty similar. They just delete an environmental variable,
attribute, or dictionary item instead of setting something. The last two
monkeypatch methods pertain to paths.
"""