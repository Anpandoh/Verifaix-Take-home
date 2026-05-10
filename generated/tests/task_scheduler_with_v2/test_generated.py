import pytest
from task_scheduler import schedule_tasks

def test_function_signature():
    """
    TP_1: Verify function signature matches schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) -> list[str]
    """
    result = schedule_tasks(['task1'], [])
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)
    
    result = schedule_tasks([], [])
    assert isinstance(result, list)

import pytest
from task_scheduler import schedule_tasks

def test_all_tasks_appear_exactly_once():
    """
    TP_2: Verify all tasks appear exactly once in the returned execution order
    """
    tasks = ['fetch_data', 'clean_data', 'train_model', 'evaluate_model']
    dependencies = [('fetch_data', 'clean_data'), ('clean_data', 'train_model'), ('train_model', 'evaluate_model')]
    result = schedule_tasks(tasks, dependencies)
    
    assert len(result) == len(tasks)
    assert set(result) == set(tasks)
    assert len(result) == len(set(result))

import pytest
from task_scheduler import schedule_tasks

def test_dependency_ordering_respected():
    """
    TP_3: Verify dependency ordering is respected for all dependency pairs
    """
    tasks = ['a', 'b', 'c', 'd']
    dependencies = [('a', 'b'), ('b', 'c'), ('c', 'd')]
    result = schedule_tasks(tasks, dependencies)
    
    for before_task, after_task in dependencies:
        before_idx = result.index(before_task)
        after_idx = result.index(after_task)
        assert before_idx < after_idx, f"{before_task} should appear before {after_task}"

import pytest
from task_scheduler import schedule_tasks

def test_lexicographic_largest_first_selection():
    """
    TP_4: Verify deterministic lexicographically largest-first selection when multiple tasks are available
    """
    result = schedule_tasks(['b', 'a', 'c'], [])
    assert result == ['c', 'b', 'a'], f"Expected ['c', 'b', 'a'], got {result}"

import pytest
from task_scheduler import schedule_tasks

def test_linear_dependency_chain():
    """
    TP_5: Verify linear dependency chain is ordered correctly
    """
    tasks = ['a', 'b', 'c', 'd']
    dependencies = [('a', 'b'), ('b', 'c'), ('c', 'd')]
    result = schedule_tasks(tasks, dependencies)
    
    assert result == ['a', 'b', 'c', 'd']

import pytest
from task_scheduler import schedule_tasks

def test_diamond_shaped_dependency_graph():
    """
    TP_6: Verify diamond-shaped dependency graph is resolved correctly
    """
    tasks = ['a', 'b', 'c', 'd']
    dependencies = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd')]
    result = schedule_tasks(tasks, dependencies)
    
    assert result.index('a') < result.index('b')
    assert result.index('a') < result.index('c')
    assert result.index('b') < result.index('d')
    assert result.index('c') < result.index('d')
    assert len(result) == 4
    assert set(result) == set(tasks)

import pytest
from task_scheduler import schedule_tasks

def test_multiple_independent_chains():
    """
    TP_7: Verify multiple independent dependency chains are ordered deterministically
    """
    tasks = ['a', 'b', 'c', 'd']
    dependencies = [('a', 'b'), ('c', 'd')]
    result = schedule_tasks(tasks, dependencies)
    
    assert result.index('a') < result.index('b')
    assert result.index('c') < result.index('d')
    assert len(result) == 4
    assert set(result) == set(tasks)

import pytest
from task_scheduler import schedule_tasks

def test_empty_tasks_and_dependencies():
    """
    TP_8: Handle empty tasks and dependencies list
    """
    result = schedule_tasks([], [])
    assert result == []

import pytest
from task_scheduler import schedule_tasks

def test_single_task_no_dependencies():
    """
    TP_9: Handle single task with no dependencies
    """
    result = schedule_tasks(['task1'], [])
    assert result == ['task1']

import pytest
from task_scheduler import schedule_tasks

def test_multiple_tasks_no_dependencies():
    """
    TP_10, TP_25: Handle multiple tasks with no dependencies
    """
    result = schedule_tasks(['x', 'y', 'z'], [])
    assert set(result) == {'x', 'y', 'z'}
    assert result == ['z', 'y', 'x']

import pytest
from task_scheduler import schedule_tasks

def test_duplicate_task_names_raises_valueerror():
    """
    TP_11: Raise ValueError for duplicate task names
    """
    with pytest.raises(ValueError, match="Duplicate task names"):
        schedule_tasks(['task1', 'task2', 'task1'], [])

import pytest
from task_scheduler import schedule_tasks

def test_unknown_task_in_dependency_raises_valueerror():
    """
    TP_12: Raise ValueError when dependency refers to unknown task
    """
    with pytest.raises(ValueError, match="Dependency refers to unknown task"):
        schedule_tasks(['task1', 'task2'], [('task1', 'unknown_task')])
    
    with pytest.raises(ValueError, match="Dependency refers to unknown task"):
        schedule_tasks(['task1', 'task2'], [('unknown_task', 'task2')])

import pytest
from task_scheduler import schedule_tasks

def test_circular_dependency_raises_valueerror():
    """
    TP_13: Raise ValueError for circular dependency
    """
    with pytest.raises(ValueError, match="Circular dependency exists"):
        schedule_tasks(['a', 'b', 'c'], [('a', 'b'), ('b', 'c'), ('c', 'a')])

import pytest
from task_scheduler import schedule_tasks

def test_tasks_not_list_raises_typeerror():
    """
    TP_14: Raise TypeError when tasks parameter is not a list
    """
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks(('task1', 'task2'), [])
    
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks('task1', [])
    
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks({'task1': 1}, [])

import pytest
from task_scheduler import schedule_tasks

def test_dependencies_not_list_raises_typeerror():
    """
    TP_15: Raise TypeError when dependencies parameter is not a list
    """
    with pytest.raises(TypeError, match="dependencies must be a list"):
        schedule_tasks(['task1'], ('task1', 'task2'))
    
    with pytest.raises(TypeError, match="dependencies must be a list"):
        schedule_tasks(['task1'], {'task1': 'task2'})

import pytest
from task_scheduler import schedule_tasks

def test_task_name_not_string_raises_typeerror():
    """
    TP_16: Raise TypeError when task name is not a string
    """
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks(['task1', 123], [])
    
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks(['task1', None], [])
    
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks(['task1', ['nested']], [])

import pytest
from task_scheduler import schedule_tasks

def test_dependency_not_pair_of_strings_raises_typeerror():
    """
    TP_17: Raise TypeError when dependency is not a pair of strings
    """
    with pytest.raises(TypeError, match="Dependency must be a pair of strings"):
        schedule_tasks(['task1', 'task2'], [('task1',)])
    
    with pytest.raises(TypeError, match="Dependency must be a pair of strings"):
        schedule_tasks(['task1', 'task2'], [('task1', 'task2', 'task3')])
    
    with pytest.raises(TypeError, match="Dependency must be a pair of strings"):
        schedule_tasks(['task1', 'task2'], [(123, 'task2')])
    
    with pytest.raises(TypeError, match="Dependency must be a pair of strings"):
        schedule_tasks(['task1', 'task2'], [('task1', 456)])

import pytest
from task_scheduler import schedule_tasks

def test_task_names_case_sensitive():
    """
    TP_18: Verify task names are case-sensitive
    """
    tasks = ['Task', 'task', 'TASK']
    dependencies = []
    result = schedule_tasks(tasks, dependencies)
    
    assert len(result) == 3
    assert 'Task' in result
    assert 'task' in result
    assert 'TASK' in result

import pytest
from task_scheduler import schedule_tasks

def test_function_does_not_execute_tasks():
    """
    TP_19: Verify function does not execute tasks or modify external state
    """
    execution_log = []
    
    def mock_task():
        execution_log.append('executed')
    
    tasks = ['task1', 'task2']
    dependencies = [('task1', 'task2')]
    result = schedule_tasks(tasks, dependencies)
    
    assert execution_log == []
    assert result == ['task1', 'task2']

import pytest
import time
from task_scheduler import schedule_tasks

def test_performance_large_task_set():
    """
    TP_20, TP_21: Verify performance meets O((N + E) log N) time complexity and O(N + E) space complexity
    """
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

def test_self_loop_circular_dependency():
    """
    TP_22: Verify self-loop circular dependency is detected
    """
    with pytest.raises(ValueError, match="Circular dependency exists"):
        schedule_tasks(['task1'], [('task1', 'task1')])

import pytest
from task_scheduler import schedule_tasks

def test_two_task_circular_dependency():
    """
    TP_23: Verify two-task circular dependency is detected
    """
    with pytest.raises(ValueError, match="Circular dependency exists"):
        schedule_tasks(['a', 'b'], [('a', 'b'), ('b', 'a')])

import pytest
from task_scheduler import schedule_tasks

def test_complex_multi_task_circular_dependency():
    """
    TP_24: Verify complex multi-task circular dependency is detected
    """
    with pytest.raises(ValueError, match="Circular dependency exists"):
        schedule_tasks(['a', 'b', 'c', 'd'], [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a')])
