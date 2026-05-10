import pytest
from task_scheduler import schedule_tasks

def test_function_signature_and_return_type():
    """TP_1: Verify function signature accepts tasks list and dependencies list, returns list of strings"""
    result = schedule_tasks(['task1'], [])
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)

import pytest
from task_scheduler import schedule_tasks

def test_all_tasks_appear_exactly_once():
    """TP_2: Verify all tasks from input appear exactly once in output"""
    tasks = ['task1', 'task2', 'task3', 'task4']
    result = schedule_tasks(tasks, [])
    assert len(result) == len(tasks)
    assert set(result) == set(tasks)
    assert len(result) == len(set(result))

import pytest
from task_scheduler import schedule_tasks

def test_simple_linear_dependency_chain():
    """TP_3: Verify dependency ordering is respected for simple linear chain"""
    tasks = ['fetch_data', 'clean_data', 'train_model', 'evaluate_model']
    dependencies = [
        ('fetch_data', 'clean_data'),
        ('clean_data', 'train_model'),
        ('train_model', 'evaluate_model')
    ]
    result = schedule_tasks(tasks, dependencies)
    assert result.index('fetch_data') < result.index('clean_data')
    assert result.index('clean_data') < result.index('train_model')
    assert result.index('train_model') < result.index('evaluate_model')

import pytest
from task_scheduler import schedule_tasks

def test_lexicographic_ordering_no_dependencies():
    """TP_4: Verify lexicographically largest task is selected first when multiple tasks are available"""
    result = schedule_tasks(['b', 'a', 'c'], [])
    assert result == ['c', 'b', 'a']

import pytest
from task_scheduler import schedule_tasks

def test_deterministic_output():
    """TP_5: Verify deterministic output across multiple invocations with same input"""
    tasks = ['x', 'y', 'z', 'a', 'b']
    dependencies = [('x', 'y'), ('y', 'z')]
    result1 = schedule_tasks(tasks, dependencies)
    result2 = schedule_tasks(tasks, dependencies)
    result3 = schedule_tasks(tasks, dependencies)
    assert result1 == result2
    assert result2 == result3

import pytest
from task_scheduler import schedule_tasks

def test_empty_tasks_and_dependencies():
    """TP_6: Verify empty tasks and dependencies returns empty list"""
    result = schedule_tasks([], [])
    assert result == []

import pytest
from task_scheduler import schedule_tasks

def test_single_task_no_dependencies():
    """TP_7: Verify single task with no dependencies returns that task"""
    result = schedule_tasks(['task1'], [])
    assert result == ['task1']

import pytest
from task_scheduler import schedule_tasks

def test_multiple_independent_tasks_lexicographic_order():
    """TP_8: Verify multiple independent tasks return in lexicographic order (largest first)"""
    result = schedule_tasks(['x', 'y', 'z'], [])
    assert result == ['z', 'y', 'x']

import pytest
from task_scheduler import schedule_tasks

def test_long_linear_dependency_chain():
    """TP_9: Verify long linear dependency chain maintains correct order"""
    tasks = ['a', 'b', 'c', 'd', 'e']
    dependencies = [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')]
    result = schedule_tasks(tasks, dependencies)
    assert result == ['a', 'b', 'c', 'd', 'e']

import pytest
from task_scheduler import schedule_tasks

def test_multiple_independent_chains():
    """TP_10: Verify multiple independent dependency chains are ordered deterministically"""
    tasks = ['a', 'b', 'c', 'd']
    dependencies = [('a', 'b'), ('c', 'd')]
    result = schedule_tasks(tasks, dependencies)
    assert result.index('a') < result.index('b')
    assert result.index('c') < result.index('d')
    assert len(result) == 4
    assert set(result) == set(tasks)

import pytest
from task_scheduler import schedule_tasks

def test_diamond_shaped_dependency_graph():
    """TP_11: Verify diamond-shaped dependency graph resolves correctly"""
    tasks = ['a', 'b', 'c', 'd']
    dependencies = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd')]
    result = schedule_tasks(tasks, dependencies)
    assert result.index('a') < result.index('b')
    assert result.index('a') < result.index('c')
    assert result.index('b') < result.index('d')
    assert result.index('c') < result.index('d')

import pytest
from task_scheduler import schedule_tasks

def test_duplicate_task_names_raises_valueerror():
    """TP_12: Verify ValueError raised for duplicate task names"""
    with pytest.raises(ValueError, match="Duplicate task names"):
        schedule_tasks(['task1', 'task1'], [])

import pytest
from task_scheduler import schedule_tasks

def test_unknown_task_in_dependency_raises_valueerror():
    """TP_13: Verify ValueError raised when dependency references unknown task"""
    with pytest.raises(ValueError, match="Dependency refers to unknown task"):
        schedule_tasks(['a', 'b'], [('a', 'unknown')])

import pytest
from task_scheduler import schedule_tasks

def test_circular_dependency_raises_valueerror():
    """TP_14: Verify ValueError raised for circular dependency"""
    with pytest.raises(ValueError, match="Circular dependency exists"):
        schedule_tasks(['a', 'b'], [('a', 'b'), ('b', 'a')])

import pytest
from task_scheduler import schedule_tasks

def test_tasks_not_list_raises_typeerror():
    """TP_15: Verify TypeError raised when tasks parameter is not a list"""
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks('not_a_list', [])

import pytest
from task_scheduler import schedule_tasks

def test_dependencies_not_list_raises_typeerror():
    """TP_16: Verify TypeError raised when dependencies parameter is not a list"""
    with pytest.raises(TypeError, match="dependencies must be a list"):
        schedule_tasks(['a'], 'not_a_list')

import pytest
from task_scheduler import schedule_tasks

def test_task_name_not_string_raises_typeerror():
    """TP_17: Verify TypeError raised when task name is not a string"""
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks([1, 2, 3], [])

import pytest
from task_scheduler import schedule_tasks

def test_dependency_not_pair_of_strings_raises_typeerror():
    """TP_18: Verify TypeError raised when dependency is not a pair of strings"""
    with pytest.raises(TypeError, match="Dependency must be a pair of strings"):
        schedule_tasks(['a', 'b'], [('a',)])

import pytest
from task_scheduler import schedule_tasks

def test_case_sensitive_task_names():
    """TP_19: Verify task names are case-sensitive"""
    tasks = ['Task', 'task']
    result = schedule_tasks(tasks, [])
    assert len(result) == 2
    assert 'Task' in result
    assert 'task' in result
    assert result != ['task', 'Task']

import pytest
from task_scheduler import schedule_tasks

def test_function_returns_ordering_only():
    """TP_20: Verify function returns ordering only without executing tasks"""
    tasks = ['task1', 'task2', 'task3']
    dependencies = [('task1', 'task2'), ('task2', 'task3')]
    result = schedule_tasks(tasks, dependencies)
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)
    assert len(result) == 3

import pytest
from task_scheduler import schedule_tasks

def test_self_referential_dependency_raises_valueerror():
    """TP_21: Verify self-referential dependency raises ValueError"""
    with pytest.raises(ValueError, match="Circular dependency exists"):
        schedule_tasks(['a'], [('a', 'a')])

import pytest
from task_scheduler import schedule_tasks

def test_complex_graph_multiple_paths():
    """TP_22: Verify complex graph with multiple paths to same node"""
    tasks = ['a', 'b', 'c', 'd', 'e']
    dependencies = [('a', 'c'), ('b', 'c'), ('c', 'd'), ('c', 'e')]
    result = schedule_tasks(tasks, dependencies)
    assert result.index('a') < result.index('c')
    assert result.index('b') < result.index('c')
    assert result.index('c') < result.index('d')
    assert result.index('c') < result.index('e')
