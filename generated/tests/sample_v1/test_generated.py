import pytest
from task_scheduler import schedule_tasks

def test_function_signature():
    """TP_1: Verify function signature matches schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) -> list[str]"""
    result = schedule_tasks(['task1'], [])
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)

import pytest
from task_scheduler import schedule_tasks

def test_basic_linear_dependency_chain():
    """TP_2: Verify basic linear dependency chain is ordered correctly"""
    tasks = ['fetch_data', 'clean_data', 'train_model', 'evaluate_model']
    dependencies = [('fetch_data', 'clean_data'), ('clean_data', 'train_model'), ('train_model', 'evaluate_model')]
    result = schedule_tasks(tasks, dependencies)
    assert result == ['fetch_data', 'clean_data', 'train_model', 'evaluate_model']

import pytest
from task_scheduler import schedule_tasks

def test_all_tasks_appear_exactly_once():
    """TP_3: Verify every task in input appears exactly once in output"""
    tasks = ['task_a', 'task_b', 'task_c', 'task_d']
    dependencies = [('task_a', 'task_b'), ('task_c', 'task_d')]
    result = schedule_tasks(tasks, dependencies)
    assert len(result) == len(tasks)
    assert set(result) == set(tasks)
    assert len(result) == len(set(result))

import pytest
from task_scheduler import schedule_tasks

def test_dependency_ordering_constraint():
    """TP_4: Verify dependency ordering constraint: for each (A, B) pair, A appears before B"""
    tasks = ['a', 'b', 'c', 'd', 'e']
    dependencies = [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e'), ('a', 'e')]
    result = schedule_tasks(tasks, dependencies)
    for before_task, after_task in dependencies:
        assert result.index(before_task) < result.index(after_task)

import pytest
from task_scheduler import schedule_tasks

def test_lexicographic_ordering_no_dependencies():
    """TP_5: Verify lexicographic ordering when multiple tasks are available"""
    result = schedule_tasks(['b', 'a', 'c'], [])
    assert result == ['a', 'b', 'c']

import pytest
from task_scheduler import schedule_tasks

def test_deterministic_output():
    """TP_6: Verify deterministic output across multiple invocations"""
    tasks = ['z', 'y', 'x', 'w']
    dependencies = [('z', 'y'), ('y', 'x')]
    result1 = schedule_tasks(tasks, dependencies)
    result2 = schedule_tasks(tasks, dependencies)
    result3 = schedule_tasks(tasks, dependencies)
    assert result1 == result2 == result3

import pytest
from task_scheduler import schedule_tasks

def test_empty_input():
    """TP_7: Verify empty input returns empty output"""
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
    """TP_9: Verify multiple independent tasks return lexicographic order"""
    result = schedule_tasks(['z', 'a', 'm'], [])
    assert result == ['a', 'm', 'z']

import pytest
from task_scheduler import schedule_tasks

def test_long_linear_dependency_chain():
    """TP_10: Verify long linear dependency chain maintains order"""
    tasks = ['task_1', 'task_2', 'task_3', 'task_4', 'task_5', 'task_6', 'task_7', 'task_8']
    dependencies = [('task_1', 'task_2'), ('task_2', 'task_3'), ('task_3', 'task_4'), ('task_4', 'task_5'), ('task_5', 'task_6'), ('task_6', 'task_7'), ('task_7', 'task_8')]
    result = schedule_tasks(tasks, dependencies)
    assert result == tasks

import pytest
from task_scheduler import schedule_tasks

def test_diamond_dependency_graph():
    """TP_11: Verify diamond-shaped dependency graph resolves correctly"""
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

def test_multiple_independent_chains():
    """TP_12: Verify multiple independent chains with lexicographic tie-breaking"""
    tasks = ['a', 'b', 'c', 'd', 'e', 'f']
    dependencies = [('a', 'b'), ('b', 'c'), ('d', 'e'), ('e', 'f')]
    result = schedule_tasks(tasks, dependencies)
    assert result.index('a') < result.index('b') < result.index('c')
    assert result.index('d') < result.index('e') < result.index('f')
    assert result.index('a') < result.index('d')

import pytest
from task_scheduler import schedule_tasks

def test_duplicate_task_names_raises_valueerror():
    """TP_13: Verify ValueError raised for duplicate task names"""
    with pytest.raises(ValueError, match="Duplicate task names"):
        schedule_tasks(['task1', 'task2', 'task1'], [])

import pytest
from task_scheduler import schedule_tasks

def test_unknown_task_in_dependency_raises_valueerror():
    """TP_14: Verify ValueError raised when dependency references unknown task"""
    with pytest.raises(ValueError, match="Dependency refers to unknown task"):
        schedule_tasks(['task1', 'task2'], [('task1', 'unknown_task')])
    with pytest.raises(ValueError, match="Dependency refers to unknown task"):
        schedule_tasks(['task1', 'task2'], [('unknown_task', 'task2')])

import pytest
from task_scheduler import schedule_tasks

def test_circular_dependency_raises_valueerror():
    """TP_15: Verify ValueError raised for circular dependency"""
    with pytest.raises(ValueError, match="Circular dependency exists"):
        schedule_tasks(['a', 'b', 'c'], [('a', 'b'), ('b', 'c'), ('c', 'a')])

import pytest
from task_scheduler import schedule_tasks

def test_tasks_not_list_raises_typeerror():
    """TP_16: Verify TypeError raised when tasks parameter is not a list"""
    with pytest.raises(TypeError, match="tasks is not a list"):
        schedule_tasks(('task1', 'task2'), [])
    with pytest.raises(TypeError, match="tasks is not a list"):
        schedule_tasks('task1', [])
    with pytest.raises(TypeError, match="tasks is not a list"):
        schedule_tasks({'task1': 1}, [])

import pytest
from task_scheduler import schedule_tasks

def test_dependencies_not_list_raises_typeerror():
    """TP_17: Verify TypeError raised when dependencies parameter is not a list"""
    with pytest.raises(TypeError, match="dependencies is not a list"):
        schedule_tasks(['task1'], ('task1', 'task2'))
    with pytest.raises(TypeError, match="dependencies is not a list"):
        schedule_tasks(['task1'], 'dependency')

import pytest
from task_scheduler import schedule_tasks

def test_task_name_not_string_raises_typeerror():
    """TP_18: Verify TypeError raised when task name is not a string"""
    with pytest.raises(TypeError, match="Task name is not a string"):
        schedule_tasks(['task1', 123], [])
    with pytest.raises(TypeError, match="Task name is not a string"):
        schedule_tasks(['task1', None], [])
    with pytest.raises(TypeError, match="Task name is not a string"):
        schedule_tasks([1, 2, 3], [])

import pytest
from task_scheduler import schedule_tasks

def test_dependency_not_pair_of_strings_raises_typeerror():
    """TP_19: Verify TypeError raised when dependency is not a pair of strings"""
    with pytest.raises(TypeError, match="Dependency is not a pair of strings"):
        schedule_tasks(['task1', 'task2'], [('task1', 123)])
    with pytest.raises(TypeError, match="Dependency is not a pair of strings"):
        schedule_tasks(['task1', 'task2'], [(123, 'task2')])
    with pytest.raises(TypeError, match="Dependency is not a pair of strings"):
        schedule_tasks(['task1', 'task2'], [('task1', 'task2', 'extra')])
    with pytest.raises(TypeError, match="Dependency is not a pair of strings"):
        schedule_tasks(['task1', 'task2'], [('task1',)])

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
    tasks = ['fetch_data', 'clean_data', 'train_model']
    dependencies = [('fetch_data', 'clean_data'), ('clean_data', 'train_model')]
    result = schedule_tasks(tasks, dependencies)
    assert isinstance(result, list)
    assert result == ['fetch_data', 'clean_data', 'train_model']
    assert all(isinstance(task, str) for task in result)

import pytest
from task_scheduler import schedule_tasks

def test_self_dependency_raises_valueerror():
    """TP_22: Verify self-dependency is detected as circular"""
    with pytest.raises(ValueError, match="Circular dependency exists"):
        schedule_tasks(['task1', 'task2'], [('task1', 'task1')])

import pytest
from task_scheduler import schedule_tasks

def test_complex_multi_level_dependency_graph():
    """TP_23: Verify complex multi-level dependency graph"""
    tasks = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    dependencies = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd'), ('d', 'e'), ('e', 'f'), ('e', 'g')]
    result = schedule_tasks(tasks, dependencies)
    for before_task, after_task in dependencies:
        assert result.index(before_task) < result.index(after_task)

import pytest
from task_scheduler import schedule_tasks

def test_empty_dependencies_multiple_tasks():
    """TP_24: Verify empty dependencies list with multiple tasks"""
    result = schedule_tasks(['zebra', 'apple', 'monkey', 'banana'], [])
    assert result == ['apple', 'banana', 'monkey', 'zebra']

import pytest
from task_scheduler import schedule_tasks
import time

def test_large_task_count_performance():
    """TP_25: Verify performance with large task count"""
    n = 1000
    tasks = [f'task_{i}' for i in range(n)]
    dependencies = [(f'task_{i}', f'task_{i+1}') for i in range(n-1)]
    start_time = time.time()
    result = schedule_tasks(tasks, dependencies)
    elapsed_time = time.time() - start_time
    assert len(result) == n
    assert result == tasks
    assert elapsed_time < 5.0
