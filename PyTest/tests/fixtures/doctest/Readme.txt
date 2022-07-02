The doctest module is part of the standard Python library and allows you to put little code examples inside docstrings for a function and test them to make sure they work. You can have pytest look for and run doctest tests within your Python code by using the --doctest-modules flag. With the doctest_namespace builtin fixture, you can build autouse fixtures to add symbols to the namespace pytest uses while running doctest tests. This allows docstrings to be much more readable. doctest_namespace is commonly used to add module imports into the namespace, especially when Python convention is to shorten the module or package name. For instance, numpy is often imported with import numpy as np.

Let’s say we have a module named unnecessary_math.py with multiply() and divide() methods that we really want to make sure everyone understands clearly. So we throw some usage examples in both the file docstring and the docstrings of the functions:

Since the name unnecessary_math is long, we decide to use um instead by using import unnecessary_math as um in the top docstring. The code in the docstrings of the functions doesn’t include the import statement, but continue with the um convention. The problem is that pytest treats each docstring with code as a different test. The import in the top docstring will allow the first part to pass, but the code in the docstrings of the functions will fail: unnecessary_math_1.py

One way to fix it is to put the import statement in each docstring: unnecessary_math_2.py

However, it also clutters the docstrings, and doesn’t add any real value to readers of the code.

The builtin fixture doctest_namespace, used in an autouse fixture at a top-level conftest.py file, will fix the problem without changing the source code: