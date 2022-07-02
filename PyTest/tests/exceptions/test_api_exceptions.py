"""Test for expected exceptions from using the API wrong."""

import pytest
import tasks


def test_add_raises():
    """add() should raise an exception with wrong type param."""
    with pytest.raises(TypeError):
        tasks.add(task='not a Task object')


"""
In test_add_raises(), the with pytest.raises(TypeError): statement says that whatever is in the next block of code should raise a TypeError exception. 
If no exception is raised, the test fails. If the test raises a different exception, it fails.
"""

@pytest.mark.smoke
def test_list_raises():
    """list() should raise an exception with wrong type param."""
    with pytest.raises(TypeError):
        tasks.list_tasks(owner=123)


@pytest.mark.get
@pytest.mark.smoke
def test_get_raises():
    """get() should raise an exception with wrong type param."""
    with pytest.raises(TypeError):
        tasks.get(task_id='123')


class TestUpdate():
    """Test expected exceptions with tasks.update()."""

    def test_bad_id(self):
        """A non-int id should raise an excption."""
        with pytest.raises(TypeError):
            tasks.update(task_id={'dict instead': 1},
                         task=tasks.Task())

    def test_bad_task(self):
        """A non-Task task should raise an excption."""
        with pytest.raises(TypeError):
            tasks.update(task_id=1, task='not a task')


def test_delete_raises():
    """delete() should raise an exception with wrong type param."""
    with pytest.raises(TypeError):
        tasks.delete(task_id=(1, 2, 3))


def test_start_tasks_db_raises():
    """Make sure unsupported db raises an exception."""
    with pytest.raises(ValueError) as excinfo:
        tasks.start_tasks_db('some/great/path', 'mysql')
    exception_msg = excinfo.value.args[0]
    assert exception_msg == "db_type must be a 'tiny' or 'mongo'"

"""
We just checked for the type of exception in test_add_raises(). 
You can also check the parameters to the exception. For start_tasks_db(db_path, db_type), not only does db_type need to be a string, it really has to be either ’tiny’ or ’mongo’. 
You can check to make sure the exception message is correct by adding as excinfo:

This allows us to look at the exception more closely. The variable name you put after as (excinfo in this case) is filled with information about the exception, and is of type ExceptionInfo.

In our case, we want to make sure the first (and only) parameter to the exception matches a string.
"""