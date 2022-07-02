import sys
import pytest
import random

"""
The capsys builtin fixture provides two bits of functionality: it allows you
to retrieve stdout and stderr from some code, and it disables output capture
temporarily. Let’s take a look at retrieving stdout and stderr
"""

def greeting(name):
    print('Hi, {}'.format(name))


def test_greeting(capsys):
    greeting('Earthling')
    out, err = capsys.readouterr()
    assert out == 'Hi, Earthling\n'
    assert err == ''

    greeting('Brian')
    greeting('Nerd')
    out, err = capsys.readouterr()
    assert out == 'Hi, Brian\nHi, Nerd\n'
    assert err == ''


def yikes(problem):
    print('YIKES! {}'.format(problem), file=sys.stderr)


def test_yikes(capsys):
    yikes('Out of coffee!')
    out, err = capsys.readouterr()
    assert out == ''
    assert 'Out of coffee!' in err

"""
pytest usually captures the output from your tests and the code under test.
This includes print statements. The captured output is displayed for failing
tests only after the full test session is complete. The -s option turns off
this feature, and output is sent to stdout while the tests are running.
Usually this works great, as it’s the output from the failed tests you need
to see in order to debug the failures. However, you may want to allow some
output to make it through the default pytest output capture, to print some
things without printing everything. You can do this with capsys. You can use
capsys.disabled() to temporarily let output get past the capture mechanism.

As you can see, always print this shows up with or without output capturing,
since it’s being printed from within a with capsys.disabled() block. The
other print statement is just a normal print statement, so normal print,
usually captured is only seen in the output when we pass in the -s flag,
which is a shortcut for --capture=no, turning off output capture.
"""

def test_capsys_disabled(capsys):
    with capsys.disabled():
        print('\nalways print this')
    print('normal print, usually captured')



@pytest.mark.parametrize('i', range(40))
def test_for_fun(i, capsys):
    if random.randint(1, 10) == 2:
        with capsys.disabled():
            sys.stdout.write('F')
