"""
The tmpdir and tmpdir_factory builtin fixtures are used to create a temporary file system directory before your test runs, and remove the directory when your test is finished.
In the Tasks project, we needed a directory to store the temporary database files used by MongoDB and TinyDB.
However, because we want to test with temporary databases that don’t survive past a test session, we used tmpdir and tmpdir_factory to do the directory creation and cleanup for us

If you’re testing something that reads, writes, or modifies files, you can use 
    ->tmpdir to create files or directories used by a single test
    ->tmpdir_factory when you want to set up a directory for many tests

The tmpdir fixture has function scope, and the tmpdir_factory fixture has session scope
Because the tmpdir fixture is defined as function scope, you can’t use tmpdir to create folders or files that should stay in place longer than one test function. 
For fixtures with scope other than function (class, module, session), tmpdir_factory is available
"""

def test_tmpdir(tmpdir):
    # tmpdir already has a path name associated with it
    # join() extends the path to include a filename
    # the file is created when it's written to
    a_file = tmpdir.join('something.txt')

    # you can create directories
    a_sub_dir = tmpdir.mkdir('anything')

    # you can create files in directories (created when written)
    another_file = a_sub_dir.join('something_else.txt')

    # this write creates 'something.txt'
    a_file.write('contents may settle during shipping')

    # this write creates 'anything/something_else.txt'
    another_file.write('something different')

    # you can read the files as well
    assert a_file.read() == 'contents may settle during shipping'
    assert another_file.read() == 'something different'


def test_tmpdir_factory(tmpdir_factory):
    # you should start with making a directory
    # a_dir acts like the object returned from the tmpdir fixture
    a_dir = tmpdir_factory.mktemp('mydir')

    # base_temp will be the parent dir of 'mydir'
    # you don't have to use getbasetemp()
    # using it here just to show that it's available
    base_temp = tmpdir_factory.getbasetemp()
    print('base:', base_temp) #You can also specify your own base directory if you need to with pytest --basetemp=mydir

    # the rest of this test looks the same as the 'test_tmpdir()'
    # example except I'm using a_dir instead of tmpdir

    a_file = a_dir.join('something.txt')
    a_sub_dir = a_dir.mkdir('anything')
    another_file = a_sub_dir.join('something_else.txt')

    a_file.write('contents may settle during shipping')
    another_file.write('something different')

    assert a_file.read() == 'contents may settle during shipping'
    assert another_file.read() == 'something different'
