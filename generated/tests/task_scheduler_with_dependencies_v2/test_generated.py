import pytest
from task_scheduler import schedule_tasks

def test_function_signature():
    """TP_1: Verify function signature matches schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) -> list[str]"""
    result = schedule_tasks(['task1'], [])
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)
    assert len(result) == 1
    assert result[0] == 'task1'

import pytest
from task_scheduler import schedule_tasks

def test_linear_dependency_chain_example():
    """TP_2: Verify linear dependency chain execution order"""
    tasks = ['fetch_data', 'clean_data', 'train_model', 'evaluate_model']
    dependencies = [('fetch_data', 'clean_data'), ('clean_data', 'train_model'), ('train_model', 'evaluate_model')]
    result = schedule_tasks(tasks, dependencies)
    assert result == ['fetch_data', 'clean_data', 'train_model', 'evaluate_model']

import pytest
from task_scheduler import schedule_tasks

def test_all_tasks_appear_exactly_once():
    """TP_3: Verify every task appears exactly once in output"""
    tasks = ['task_a', 'task_b', 'task_c', 'task_d']
    dependencies = [('task_a', 'task_b'), ('task_b', 'task_c')]
    result = schedule_tasks(tasks, dependencies)
    assert len(result) == len(tasks)
    assert set(result) == set(tasks)
    assert len(result) == len(set(result))

import pytest
from task_scheduler import schedule_tasks

def test_dependency_ordering_constraint():
    """TP_4: Verify dependency ordering constraint is satisfied"""
    tasks = ['a', 'b', 'c', 'd', 'e']
    dependencies = [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')]
    result = schedule_tasks(tasks, dependencies)
    for before_task, after_task in dependencies:
        before_idx = result.index(before_task)
        after_idx = result.index(after_task)
        assert before_idx < after_idx, f"{before_task} should appear before {after_task}"

import pytest
from task_scheduler import schedule_tasks

def test_lexicographic_largest_first():
    """TP_5: Verify lexicographically largest task selected first when multiple available"""
    result = schedule_tasks(['b', 'a', 'c'], [])
    assert result == ['c', 'b', 'a']

import pytest
from task_scheduler import schedule_tasks

def test_deterministic_output():
    """TP_6: Verify deterministic output across multiple invocations"""
    tasks = ['x', 'y', 'z', 'w']
    dependencies = [('x', 'y'), ('z', 'w')]
    result1 = schedule_tasks(tasks, dependencies)
    result2 = schedule_tasks(tasks, dependencies)
    result3 = schedule_tasks(tasks, dependencies)
    assert result1 == result2
    assert result2 == result3

import pytest
from task_scheduler import schedule_tasks

def test_empty_tasks_and_dependencies():
    """TP_7: Verify empty tasks and dependencies returns empty list"""
    result = schedule_tasks([], [])
    assert result == []

import pytest
from task_scheduler import schedule_tasks

def test_single_task_no_dependencies():
    """TP_8: Verify single task with no dependencies returns that task"""
    result = schedule_tasks(['task1'], [])
    assert result == ['task1']

import pytest
from task_scheduler import schedule_tasks

def test_multiple_independent_tasks_lexicographic():
    """TP_9: Verify multiple independent tasks return lexicographic order (largest first)"""
    result = schedule_tasks(['x', 'y', 'z'], [])
    assert result == ['z', 'y', 'x']

import pytest
from task_scheduler import schedule_tasks

def test_long_linear_dependency_chain():
    """TP_10: Verify long linear dependency chain maintains correct order"""
    tasks = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8']
    dependencies = [(tasks[i], tasks[i+1]) for i in range(len(tasks)-1)]
    result = schedule_tasks(tasks, dependencies)
    assert result == tasks

import pytest
from task_scheduler import schedule_tasks

def test_multiple_independent_chains():
    """TP_11: Verify multiple independent chains with deterministic ordering"""
    tasks = ['a', 'b', 'c', 'd', 'e', 'f']
    dependencies = [('a', 'b'), ('b', 'c'), ('d', 'e'), ('e', 'f')]
    result = schedule_tasks(tasks, dependencies)
    assert result.index('a') < result.index('b') < result.index('c')
    assert result.index('d') < result.index('e') < result.index('f')
    assert len(result) == 6
    assert set(result) == set(tasks)

import pytest
from task_scheduler import schedule_tasks

def test_diamond_shaped_dependency_graph():
    """TP_12: Verify diamond-shaped dependency graph resolves correctly"""
    tasks = ['a', 'b', 'c', 'd']
    dependencies = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd')]
    result = schedule_tasks(tasks, dependencies)
    assert result == ['a', 'b', 'c', 'd']
    assert result.index('a') < result.index('b')
    assert result.index('a') < result.index('c')
    assert result.index('b') < result.index('d')
    assert result.index('c') < result.index('d')

import pytest
from task_scheduler import schedule_tasks

def test_duplicate_task_names_raises_error():
    """TP_13: Verify ValueError raised for duplicate task names"""
    with pytest.raises(ValueError, match="Duplicate task names"):
        schedule_tasks(['task1', 'task2', 'task1'], [])

import pytest
from task_scheduler import schedule_tasks

def test_unknown_task_in_dependency_raises_error():
    """TP_14: Verify ValueError raised for dependency referencing unknown task"""
    with pytest.raises(ValueError, match="unknown task"):
        schedule_tasks(['task1', 'task2'], [('task1', 'unknown_task')])
    with pytest.raises(ValueError, match="unknown task"):
        schedule_tasks(['task1', 'task2'], [('unknown_task', 'task2')])

import pytest
from task_scheduler import schedule_tasks

def test_circular_dependency_raises_error():
    """TP_15: Verify ValueError raised for circular dependency"""
    with pytest.raises(ValueError, match="Circular dependency"):
        schedule_tasks(['a', 'b', 'c'], [('a', 'b'), ('b', 'c'), ('c', 'a')])

import pytest
from task_scheduler import schedule_tasks

def test_tasks_not_list_raises_error():
    """TP_16: Verify TypeError raised when tasks is not a list"""
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks('not_a_list', [])
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks(('task1', 'task2'), [])
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks({'task1', 'task2'}, [])

import pytest
from task_scheduler import schedule_tasks

def test_dependencies_not_list_raises_error():
    """TP_17: Verify TypeError raised when dependencies is not a list"""
    with pytest.raises(TypeError, match="dependencies must be a list"):
        schedule_tasks(['task1'], 'not_a_list')
    with pytest.raises(TypeError, match="dependencies must be a list"):
        schedule_tasks(['task1'], {('task1', 'task2')})

import pytest
from task_scheduler import schedule_tasks

def test_task_name_not_string_raises_error():
    """TP_18: Verify TypeError raised when task name is not a string"""
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks(['task1', 123, 'task3'], [])
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks([None, 'task2'], [])
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks(['task1', ['nested']], [])

import pytest
from task_scheduler import schedule_tasks

def test_dependency_not_pair_of_strings_raises_error():
    """TP_19: Verify TypeError raised when dependency is not a pair of strings"""
    with pytest.raises(TypeError, match="Dependency must be"):
        schedule_tasks(['task1', 'task2'], [('task1',)])
    with pytest.raises(TypeError, match="Dependency must be"):
        schedule_tasks(['task1', 'task2'], [('task1', 'task2', 'extra')])
    with pytest.raises(TypeError, match="Dependency must be"):
        schedule_tasks(['task1', 'task2'], [(123, 'task2')])
    with pytest.raises(TypeError, match="Dependency must be"):
        schedule_tasks(['task1', 'task2'], [('task1', 456)])

import pytest
from task_scheduler import schedule_tasks

def test_case_sensitive_task_names():
    """TP_20: Verify task names are case-sensitive"""
    tasks = ['Task', 'task', 'TASK']
    dependencies = []
    result = schedule_tasks(tasks, dependencies)
    assert 'Task' in result
    assert 'task' in result
    assert 'TASK' in result
    assert len(result) == 3

import pytest
from task_scheduler import schedule_tasks

def test_function_returns_ordering_only():
    """TP_21: Verify function returns ordering only without executing tasks"""
    tasks = ['task1', 'task2', 'task3']
    dependencies = [('task1', 'task2'), ('task2', 'task3')]
    result = schedule_tasks(tasks, dependencies)
    assert isinstance(result, list)
    assert result == ['task1', 'task2', 'task3']
    assert all(isinstance(item, str) for item in result)

import pytest
import time
from task_scheduler import schedule_tasks

def test_performance_large_task_count():
    """TP_22: Verify performance with large task count"""
    n = 1000
    tasks = [f'task_{i}' for i in range(n)]
    dependencies = [(f'task_{i}', f'task_{i+1}') for i in range(n-1)]
    start_time = time.time()
    result = schedule_tasks(tasks, dependencies)
    elapsed_time = time.time() - start_time
    assert len(result) == n
    assert elapsed_time < 5.0

import pytest
from task_scheduler import schedule_tasks

def test_self_referential_dependency_raises_error():
    """TP_23: Verify self-referential dependency raises error"""
    with pytest.raises(ValueError, match="Circular dependency"):
        schedule_tasks(['task1', 'task2'], [('task1', 'task1')])
    with pytest.raises(ValueError, match="Circular dependency"):
        schedule_tasks(['a', 'b', 'c'], [('a', 'b'), ('b', 'b'), ('b', 'c')])

import pytest
from task_scheduler import schedule_tasks

def test_complex_diamond_multiple_convergence():
    """TP_24: Verify complex diamond with multiple convergence points"""
    tasks = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    dependencies = [
        ('a', 'b'), ('a', 'c'),
        ('b', 'd'), ('c', 'd'),
        ('d', 'e'), ('d', 'f'),
        ('e', 'g'), ('f', 'g')
    ]
    result = schedule_tasks(tasks, dependencies)
    assert len(result) == len(tasks)
    assert set(result) == set(tasks)
    for before_task, after_task in dependencies:
        assert result.index(before_task) < result.index(after_task)
