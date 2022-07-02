import pytest

"""
The pytestconfig fixture is a shortcut to request.config, and is sometimes
referred to in the pytest documentation as “the pytest config object. With
the pytestconfig builtin fixture, you can control how pytest runs through
command-line arguments and options, configuration files, plugins, and the
directory from which you launched pytest. 
"""
def test_option(pytestconfig):
    print('"foo" set to:', pytestconfig.getoption('foo'))
    print('"myopt" set to:', pytestconfig.getoption('myopt'))

"""
Adding command-line options via pytest_addoption should be done via plugins or
in the conftest.py file at the top of your project directory structure. You
shouldn’t do it in a test subdirectory.

Because pytestconfig is a fixture, it can also be accessed from other
fixtures. You can make fixtures for the option names, if you like, like this:
"""
@pytest.fixture()
def foo(pytestconfig):
    return pytestconfig.option.foo

@pytest.fixture()
def myopt(pytestconfig):
    return pytestconfig.option.myopt


def test_fixtures_for_options(foo, myopt):
    print('"foo" set to:', foo)
    print('"myopt" set to:', myopt)


def test_pytestconfig(pytestconfig):
    print('args            :', pytestconfig.args)
    print('inifile         :', pytestconfig.inifile)
    print('invocation_dir  :', pytestconfig.invocation_dir)
    print('rootdir         :', pytestconfig.rootdir)
    print('-k EXPRESSION   :', pytestconfig.getoption('keyword'))
    print('-v, --verbose   :', pytestconfig.getoption('verbose'))
    # print('-q, --quiet     :', pytestconfig.getoption('quiet'))
    print('-l, --showlocals:', pytestconfig.getoption('showlocals'))
    print('--tb=style      :', pytestconfig.getoption('tbstyle'))


def test_legacy(request):
    print('\n"foo" set to:', request.config.getoption('foo'))
    print('"myopt" set to:', request.config.getoption('myopt'))
    print('"keyword" set to:', request.config.getoption('keyword'))
