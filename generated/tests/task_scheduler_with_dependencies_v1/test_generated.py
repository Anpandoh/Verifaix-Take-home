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

def test_basic_linear_dependency_chain():
    """TP_2: Test basic linear dependency chain execution order"""
    tasks = ['fetch_data', 'clean_data', 'train_model', 'evaluate_model']
    dependencies = [('fetch_data', 'clean_data'),
                    ('clean_data', 'train_model'),
                    ('train_model', 'evaluate_model')]
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
    """TP_5: Test lexicographic ordering when multiple tasks are available"""
    tasks = ['b', 'a', 'c']
    dependencies = []
    result = schedule_tasks(tasks, dependencies)
    assert result == ['a', 'b', 'c']

import pytest
from task_scheduler import schedule_tasks

def test_deterministic_output_consistency():
    """TP_6: Test deterministic output consistency across multiple calls"""
    tasks = ['z', 'a', 'm', 'b']
    dependencies = [('z', 'a'), ('a', 'm')]
    result1 = schedule_tasks(tasks, dependencies)
    result2 = schedule_tasks(tasks, dependencies)
    result3 = schedule_tasks(tasks, dependencies)
    assert result1 == result2 == result3

import pytest
from task_scheduler import schedule_tasks

def test_empty_tasks_and_dependencies():
    """TP_7: Test empty tasks and dependencies boundary condition"""
    result = schedule_tasks([], [])
    assert result == []

import pytest
from task_scheduler import schedule_tasks

def test_single_task_no_dependencies():
    """TP_8: Test single task with no dependencies boundary condition"""
    result = schedule_tasks(['only_task'], [])
    assert result == ['only_task']

import pytest
from task_scheduler import schedule_tasks

def test_multiple_independent_tasks():
    """TP_9: Test multiple independent tasks with no dependencies"""
    tasks = ['zebra', 'apple', 'monkey', 'banana']
    result = schedule_tasks(tasks, [])
    assert result == ['apple', 'banana', 'monkey', 'zebra']

import pytest
from task_scheduler import schedule_tasks

def test_long_linear_dependency_chain():
    """TP_10: Test long linear dependency chain"""
    tasks = ['task_1', 'task_2', 'task_3', 'task_4', 'task_5', 'task_6', 'task_7']
    dependencies = [('task_1', 'task_2'), ('task_2', 'task_3'), ('task_3', 'task_4'),
                    ('task_4', 'task_5'), ('task_5', 'task_6'), ('task_6', 'task_7')]
    result = schedule_tasks(tasks, dependencies)
    assert result == tasks

import pytest
from task_scheduler import schedule_tasks

def test_diamond_shaped_dependency_graph():
    """TP_11: Test diamond-shaped dependency graph"""
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
    """TP_12: Test multiple independent dependency chains"""
    tasks = ['a', 'b', 'c', 'd', 'e', 'f']
    dependencies = [('a', 'b'), ('b', 'c'), ('d', 'e'), ('e', 'f')]
    result = schedule_tasks(tasks, dependencies)
    assert result.index('a') < result.index('b') < result.index('c')
    assert result.index('d') < result.index('e') < result.index('f')
    assert len(result) == 6
    assert set(result) == set(tasks)

import pytest
from task_scheduler import schedule_tasks

def test_duplicate_task_names_error():
    """TP_13: Test ValueError for duplicate task names"""
    tasks = ['task_a', 'task_b', 'task_a']
    dependencies = []
    with pytest.raises(ValueError, match="Duplicate task names found"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_unknown_task_in_dependency_error():
    """TP_14: Test ValueError for dependency referring to unknown task"""
    tasks = ['task_a', 'task_b']
    dependencies = [('task_a', 'unknown_task')]
    with pytest.raises(ValueError, match="Dependency refers to unknown task"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_circular_dependency_error():
    """TP_15: Test ValueError for circular dependency"""
    tasks = ['a', 'b', 'c']
    dependencies = [('a', 'b'), ('b', 'c'), ('c', 'a')]
    with pytest.raises(ValueError, match="Circular dependency exists"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_tasks_not_list_error():
    """TP_16: Test TypeError when tasks parameter is not a list"""
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks('not_a_list', [])
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks(('task_a', 'task_b'), [])
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks({'task_a'}, [])

import pytest
from task_scheduler import schedule_tasks

def test_dependencies_not_list_error():
    """TP_17: Test TypeError when dependencies parameter is not a list"""
    with pytest.raises(TypeError, match="dependencies must be a list"):
        schedule_tasks(['task_a'], 'not_a_list')
    with pytest.raises(TypeError, match="dependencies must be a list"):
        schedule_tasks(['task_a'], {('task_a', 'task_b')})

import pytest
from task_scheduler import schedule_tasks

def test_task_name_not_string_error():
    """TP_18: Test TypeError when task name is not a string"""
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks(['task_a', 123, 'task_c'], [])
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks(['task_a', None], [])
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks([['task_a']], [])

import pytest
from task_scheduler import schedule_tasks

def test_dependency_not_pair_of_strings_error():
    """TP_19: Test TypeError when dependency is not a pair of strings"""
    with pytest.raises(TypeError, match="Dependency must be a pair of strings"):
        schedule_tasks(['a', 'b'], [('a', 'b', 'c')])
    with pytest.raises(TypeError, match="Dependency must be a pair of strings"):
        schedule_tasks(['a', 'b'], [('a',)])
    with pytest.raises(TypeError, match="Dependency must be a pair of strings"):
        schedule_tasks(['a', 'b'], [(1, 'b')])
    with pytest.raises(TypeError, match="Dependency must be a pair of strings"):
        schedule_tasks(['a', 'b'], [('a', None)])

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
    assert result == ['TASK', 'Task', 'task']

import pytest
from task_scheduler import schedule_tasks

def test_function_returns_ordering_only():
    """TP_21: Verify function returns ordering only without executing tasks"""
    tasks = ['task_a', 'task_b', 'task_c']
    dependencies = [('task_a', 'task_b'), ('task_b', 'task_c')]
    result = schedule_tasks(tasks, dependencies)
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)
    assert result == ['task_a', 'task_b', 'task_c']

import pytest
from task_scheduler import schedule_tasks

def test_complex_graph_multiple_paths():
    """TP_22: Test complex graph with multiple paths and convergence points"""
    tasks = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    dependencies = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd'),
                    ('d', 'e'), ('e', 'f'), ('e', 'g')]
    result = schedule_tasks(tasks, dependencies)
    assert len(result) == len(tasks)
    assert set(result) == set(tasks)
    for before_task, after_task in dependencies:
        assert result.index(before_task) < result.index(after_task)

import pytest
from task_scheduler import schedule_tasks

def test_self_dependency_error():
    """TP_23: Test self-dependency error handling"""
    tasks = ['a', 'b', 'c']
    dependencies = [('a', 'a')]
    with pytest.raises(ValueError, match="Circular dependency exists"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_empty_dependencies_multiple_tasks():
    """TP_24: Test empty dependencies list with multiple tasks"""
    tasks = ['zebra', 'apple', 'monkey', 'banana', 'cat']
    result = schedule_tasks(tasks, [])
    assert result == sorted(tasks)
    assert len(result) == len(tasks)

import pytest
from task_scheduler import schedule_tasks
import time

def test_large_number_of_tasks_performance():
    """TP_25: Test large number of tasks and dependencies for performance"""
    n = 1000
    tasks = [f'task_{i}' for i in range(n)]
    dependencies = [(f'task_{i}', f'task_{i+1}') for i in range(n-1)]
    start_time = time.time()
    result = schedule_tasks(tasks, dependencies)
    elapsed_time = time.time() - start_time
    assert len(result) == n
    assert result == tasks
    assert elapsed_time < 5.0
