A “monkey patch” is a dynamic modification of a class or module during runtime. During testing, “monkey patching” is a convenient way to take over part of the runtime environment of the code under test and replace either input dependencies or output dependencies with objects or functions that are more convenient for testing. The monkeypatch builtin fixture allows you to do this in the context of a single test. And when the test ends, regardless of pass or fail, the original unpatched is restored, undoing everything changed by the patch.

The monkeypatch fixture provides the following functions:

setattr(target, name, value=<notset>, raising=True): Set an attribute.

delattr(target, name=<notset>, raising=True): Delete an attribute.

setitem(dic, name, value): Set a dictionary entry.

delitem(dic, name, raising=True): Delete a dictionary entry.

setenv(name, value, prepend=None): Set an environmental variable.

delenv(name, raising=True): Delete an environmental variable.

syspath_prepend(path): Prepend path to sys.path, which is Python’s list of import locations.

chdir(path): Change the current working directory.

The raising parameter tells pytest whether or not to raise an exception if the item doesn’t already exist. The prepend parameter to setenv() can be a character. If it is set, the value of the environmental variable will be changed to value + prepend + <old value>.

syspath_prepend(path) prepends a path to sys.path, which has the effect of putting your new path at the head of the line for module import directories. One use for this would be to replace a system-wide module or package with a stub version. You can then use monkeypatch.syspath_prepend() to prepend the directory of your stub version and the code under test will find the stub version first

chdir(path) changes the current working directory during the test. This would be useful for testing command-line scripts and other utilities that depend on what the current working directory is. You could set up a temporary directory with whatever contents make sense for your script, and then use monkeypatch.chdir(the_tmpdir)