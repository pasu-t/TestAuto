"""Test the tasks.add() API function."""

import pytest
import tasks
from tasks import Task

def test_add_1():
    """tasks.get() using id returned from add() works."""
    task = Task('breathe', 'BRIAN', True)
    task_id = tasks.add(task)
    t_from_db = tasks.get(task_id)
    # everything but the id should be the same
    assert equivalent(t_from_db, task)


def equivalent(t1, t2):
    """Check two tasks for equivalence."""
    # Compare everything but the id field
    return ((t1.summary == t2.summary) and
            (t1.owner == t2.owner) and
            (t1.done == t2.done))


@pytest.fixture(autouse=True)
def initialized_tasks_db(tmpdir):
    """Connect to db before testing, disconnect after."""
    tasks.start_tasks_db(str(tmpdir), 'tiny')
    yield
    tasks.stop_tasks_db()

'''
We can use @pytest.mark.parametrize(argnames, argvalues) to pass lots of data through the same test, like this.
The first argument to parametrize() is a string with a comma-separated list of names—’task’, in our case. 
The second argument is a list of values, which in our case is a list of Task objects. 
pytest will run this test once for each task and report each as a separate test
'''

@pytest.mark.parametrize('task',
                         [Task('sleep', done=True),
                          Task('wake', 'brian'),
                          Task('breathe', 'BRIAN', True),
                          Task('exercise', 'BrIaN', False)])
def test_add_2(task):
    """Demonstrate parametrize with one parameter."""
    task_id = tasks.add(task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, task)

"""
let’s pass in the tasks as tuples to see how multiple test parameters would work:
You can use that whole test identifier—called a node in pytest terminology—to re-run the test if you want:
pytest -v test_add_variety.py::test_add_3[sleep-None-False]
pytest -v "test_add_variety.py::test_add_3[eat eggs-BrIaN-False]
"""
@pytest.mark.parametrize('summary, owner, done',
                         [('sleep', None, False),
                          ('wake', 'brian', False),
                          ('breathe', 'BRIAN', True),
                          ('eat eggs', 'BrIaN', False),
                          ])
def test_add_3(summary, owner, done):
    """Demonstrate parametrize with multiple parameters."""
    task = Task(summary, owner, done)
    task_id = tasks.add(task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, task)

"""
Now let’s go back to the list of tasks version, but move the task list to a variable outside the function:
It’s convenient and the code looks nice. But the readability of the output is hard to interpret:
"""

tasks_to_try = (Task('sleep', done=True),
                Task('wake', 'brian'),
                Task('wake', 'brian'),
                Task('breathe', 'BRIAN', True),
                Task('exercise', 'BrIaN', False))


@pytest.mark.parametrize('task', tasks_to_try)
def test_add_4(task):
    """Slightly different take."""
    task_id = tasks.add(task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, task)

"""
The readability of the multiple parameter version is nice, but so is the list of Task objects. 
To compromise, we can use the ids optional parameter to parametrize() to make our own identifiers for each task data set. 
The ids parameter needs to be a list of strings the same length as the number of data sets. 
However, because we assigned our data set to a variable name, tasks_to_try, we can use it to generate ids:
"""

task_ids = ['Task({},{},{})'.format(t.summary, t.owner, t.done)
            for t in tasks_to_try]


@pytest.mark.parametrize('task', tasks_to_try, ids=task_ids)
def test_add_5(task):
    """Demonstrate ids."""
    task_id = tasks.add(task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, task)

"""
You can also identify parameters by including an id right alongside the parameter value when passing in a list within the @pytest.mark.parametrize() decorator. 
You do this with pytest.param(<value>, id="something"). This is useful when the id cannot be derived from the parameter value.
"""
@pytest.mark.parametrize('task', [
    pytest.param(Task('create'), id='just summary'),
    pytest.param(Task('inspire', 'Michelle'), id='summary/owner'),
    pytest.param(Task('encourage', 'Michelle', True), id='summary/owner/done')])
def test_add_6(task):
    """Demonstrate pytest.param and id."""
    task_id = tasks.add(task)
    t_from_db = tasks.get(task_id)
    assert equivalent(t_from_db, task)

"""
You can apply parametrize() to classes as well. When you do that, the same data sets will be sent to all test methods in the class:
"""

@pytest.mark.parametrize('task', tasks_to_try, ids=task_ids)
class TestAdd():
    """Demonstrate parametrize and test classes."""

    def test_equivalent(self, task):
        """Similar test, just within a class."""
        task_id = tasks.add(task)
        t_from_db = tasks.get(task_id)
        assert equivalent(t_from_db, task)

    def test_valid_id(self, task):
        """We can use the same data for multiple tests."""
        task_id = tasks.add(task)
        t_from_db = tasks.get(task_id)
        assert t_from_db.id == task_id