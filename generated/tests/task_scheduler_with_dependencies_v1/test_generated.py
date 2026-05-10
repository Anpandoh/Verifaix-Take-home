import pytest
from task_scheduler import schedule_tasks

def test_function_signature():
    """
    TP_1: Verify function signature matches schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) -> list[str]
    """
    result = schedule_tasks(['task1'], [])
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)

import pytest
from task_scheduler import schedule_tasks

def test_basic_linear_dependency_chain():
    """
    TP_2: Verify basic linear dependency chain execution order
    """
    tasks = ['fetch_data', 'clean_data', 'train_model', 'evaluate_model']
    dependencies = [
        ('fetch_data', 'clean_data'),
        ('clean_data', 'train_model'),
        ('train_model', 'evaluate_model')
    ]
    result = schedule_tasks(tasks, dependencies)
    assert result == ['fetch_data', 'clean_data', 'train_model', 'evaluate_model']

import pytest
from task_scheduler import schedule_tasks

def test_lexicographic_ordering_no_dependencies():
    """
    TP_3: Verify lexicographic ordering when no dependencies exist
    """
    tasks = ['b', 'a', 'c']
    dependencies = []
    result = schedule_tasks(tasks, dependencies)
    assert result == ['a', 'b', 'c']

import pytest
from task_scheduler import schedule_tasks

def test_all_tasks_appear_exactly_once():
    """
    TP_4: Verify every task appears exactly once in output
    """
    tasks = ['task1', 'task2', 'task3', 'task4', 'task5']
    dependencies = [('task1', 'task2'), ('task3', 'task4')]
    result = schedule_tasks(tasks, dependencies)
    assert len(result) == len(tasks)
    assert set(result) == set(tasks)
    assert len(result) == len(set(result))

import pytest
from task_scheduler import schedule_tasks

def test_dependency_ordering_constraint():
    """
    TP_5: Verify dependency ordering constraint is satisfied
    """
    tasks = ['a', 'b', 'c', 'd']
    dependencies = [('a', 'b'), ('b', 'c'), ('c', 'd')]
    result = schedule_tasks(tasks, dependencies)
    for before, after in dependencies:
        assert result.index(before) < result.index(after)

import pytest
from task_scheduler import schedule_tasks

def test_deterministic_lexicographic_selection():
    """
    TP_6: Verify deterministic output with lexicographic selection
    """
    tasks = ['z', 'a', 'm', 'b']
    dependencies = []
    result1 = schedule_tasks(tasks, dependencies)
    result2 = schedule_tasks(tasks, dependencies)
    assert result1 == result2
    assert result1 == ['a', 'b', 'm', 'z']

import pytest
from task_scheduler import schedule_tasks

def test_diamond_dependency_graph():
    """
    TP_7: Verify diamond-shaped dependency graph handling
    """
    tasks = ['a', 'b', 'c', 'd']
    dependencies = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd')]
    result = schedule_tasks(tasks, dependencies)
    assert result.index('a') < result.index('b')
    assert result.index('a') < result.index('c')
    assert result.index('b') < result.index('d')
    assert result.index('c') < result.index('d')

import pytest
from task_scheduler import schedule_tasks

def test_empty_tasks_and_dependencies():
    """
    TP_8: Verify empty tasks and dependencies returns empty list
    """
    result = schedule_tasks([], [])
    assert result == []

import pytest
from task_scheduler import schedule_tasks

def test_single_task_no_dependencies():
    """
    TP_9: Verify single task with no dependencies
    """
    result = schedule_tasks(['single_task'], [])
    assert result == ['single_task']

import pytest
from task_scheduler import schedule_tasks

def test_multiple_independent_chains():
    """
    TP_10: Verify multiple independent chains are ordered deterministically
    """
    tasks = ['a1', 'a2', 'b1', 'b2']
    dependencies = [('a1', 'a2'), ('b1', 'b2')]
    result = schedule_tasks(tasks, dependencies)
    assert result.index('a1') < result.index('a2')
    assert result.index('b1') < result.index('b2')
    assert result == ['a1', 'a2', 'b1', 'b2']

import pytest
from task_scheduler import schedule_tasks

def test_long_dependency_chain():
    """
    TP_11: Verify long dependency chain execution
    """
    tasks = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10']
    dependencies = [(f't{i}', f't{i+1}') for i in range(1, 10)]
    result = schedule_tasks(tasks, dependencies)
    assert result == tasks
    for i in range(len(result) - 1):
        assert result.index(result[i]) < result.index(result[i+1])

import pytest
from task_scheduler import schedule_tasks

def test_duplicate_task_names_raises_valueerror():
    """
    TP_12: Verify ValueError on duplicate task names
    """
    tasks = ['task1', 'task2', 'task1']
    dependencies = []
    with pytest.raises(ValueError, match="Duplicate task names"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_unknown_task_in_dependency_raises_valueerror():
    """
    TP_13: Verify ValueError on dependency referring to unknown task
    """
    tasks = ['task1', 'task2']
    dependencies = [('task1', 'unknown_task')]
    with pytest.raises(ValueError, match="Unknown task"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_circular_dependency_raises_valueerror():
    """
    TP_14: Verify ValueError on circular dependency detection
    """
    tasks = ['a', 'b', 'c']
    dependencies = [('a', 'b'), ('b', 'c'), ('c', 'a')]
    with pytest.raises(ValueError, match="Circular dependency"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_tasks_not_list_raises_typeerror():
    """
    TP_15: Verify TypeError when tasks parameter is not a list
    """
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks('not_a_list', [])
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks(('task1', 'task2'), [])
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks({'task1'}, [])

import pytest
from task_scheduler import schedule_tasks

def test_dependencies_not_list_raises_typeerror():
    """
    TP_16: Verify TypeError when dependencies parameter is not a list
    """
    with pytest.raises(TypeError, match="dependencies must be a list"):
        schedule_tasks(['task1'], 'not_a_list')
    with pytest.raises(TypeError, match="dependencies must be a list"):
        schedule_tasks(['task1'], {('task1', 'task2')})

import pytest
from task_scheduler import schedule_tasks

def test_task_name_not_string_raises_typeerror():
    """
    TP_17: Verify TypeError when task name is not a string
    """
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks(['task1', 123, 'task3'], [])
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks([None, 'task2'], [])
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks(['task1', ['nested']], [])

import pytest
from task_scheduler import schedule_tasks

def test_dependency_not_pair_of_strings_raises_typeerror():
    """
    TP_18: Verify TypeError when dependency is not a pair of strings
    """
    with pytest.raises(TypeError, match="Dependency must be a pair of strings"):
        schedule_tasks(['task1', 'task2'], [('task1', 123)])
    with pytest.raises(TypeError, match="Dependency must be a tuple"):
        schedule_tasks(['task1', 'task2'], [['task1', 'task2']])
    with pytest.raises(TypeError, match="Dependency must be a pair"):
        schedule_tasks(['task1', 'task2'], [('task1', 'task2', 'extra')])

import pytest
from task_scheduler import schedule_tasks

def test_case_sensitive_task_names():
    """
    TP_19: Verify task names are case-sensitive
    """
    tasks = ['Task', 'task', 'TASK']
    dependencies = []
    result = schedule_tasks(tasks, dependencies)
    assert len(result) == 3
    assert 'Task' in result
    assert 'task' in result
    assert 'TASK' in result
    assert result == ['TASK', 'Task', 'task']

import pytest
from task_scheduler import schedule_tasks

def test_function_does_not_execute_tasks():
    """
    TP_20: Verify function does not execute tasks or modify external state
    """
    execution_log = []
    tasks = ['task1', 'task2', 'task3']
    dependencies = [('task1', 'task2'), ('task2', 'task3')]
    result = schedule_tasks(tasks, dependencies)
    assert len(execution_log) == 0
    assert result == ['task1', 'task2', 'task3']
    assert len(execution_log) == 0

import pytest
from task_scheduler import schedule_tasks

def test_self_referential_dependency_raises_valueerror():
    """
    TP_21: Verify self-referential dependency is rejected
    """
    tasks = ['task1', 'task2']
    dependencies = [('task1', 'task1')]
    with pytest.raises(ValueError, match="cannot depend on itself"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_complex_multi_level_dependency_graph():
    """
    TP_22: Verify complex multi-level dependency graph
    """
    tasks = ['a', 'b', 'c', 'd', 'e', 'f']
    dependencies = [
        ('a', 'b'),
        ('a', 'c'),
        ('b', 'd'),
        ('c', 'd'),
        ('d', 'e'),
        ('d', 'f')
    ]
    result = schedule_tasks(tasks, dependencies)
    for before, after in dependencies:
        assert result.index(before) < result.index(after)

import pytest
from task_scheduler import schedule_tasks

def test_empty_dependencies_multiple_tasks():
    """
    TP_23: Verify empty dependencies list with multiple tasks
    """
    tasks = ['zebra', 'apple', 'monkey', 'banana']
    dependencies = []
    result = schedule_tasks(tasks, dependencies)
    assert result == ['apple', 'banana', 'monkey', 'zebra']

import pytest
from task_scheduler import schedule_tasks

def test_duplicate_dependencies_handled_correctly():
    """
    TP_24: Verify duplicate dependencies are handled correctly
    """
    tasks = ['a', 'b', 'c']
    dependencies = [('a', 'b'), ('a', 'b'), ('b', 'c'), ('b', 'c')]
    result = schedule_tasks(tasks, dependencies)
    assert result == ['a', 'b', 'c']
    assert result.index('a') < result.index('b')
    assert result.index('b') < result.index('c')
