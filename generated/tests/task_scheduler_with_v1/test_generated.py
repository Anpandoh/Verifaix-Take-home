import pytest
from task_scheduler import schedule_tasks

def test_function_exists_with_correct_signature():
    """TP_1: Verify schedule_tasks function exists with correct signature."""
    assert callable(schedule_tasks)
    result = schedule_tasks(['task1'], [])
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)

import pytest
from task_scheduler import schedule_tasks

def test_returns_all_tasks_exactly_once():
    """TP_2: Verify function returns all tasks exactly once in output."""
    tasks = ['task1', 'task2', 'task3']
    result = schedule_tasks(tasks, [])
    assert len(result) == len(tasks)
    assert set(result) == set(tasks)
    assert len(result) == len(set(result))

import pytest
from task_scheduler import schedule_tasks

def test_simple_linear_dependency_chain():
    """TP_3: Verify dependency ordering is respected for simple linear chain."""
    tasks = ['fetch_data', 'clean_data', 'train_model', 'evaluate_model']
    dependencies = [
        ('fetch_data', 'clean_data'),
        ('clean_data', 'train_model'),
        ('train_model', 'evaluate_model')
    ]
    result = schedule_tasks(tasks, dependencies)
    assert result == ['fetch_data', 'clean_data', 'train_model', 'evaluate_model']
    for before, after in dependencies:
        assert result.index(before) < result.index(after)

import pytest
from task_scheduler import schedule_tasks

def test_lexicographic_ordering_no_dependencies():
    """TP_4: Verify lexicographic ordering when multiple tasks are available."""
    tasks = ['b', 'a', 'c']
    result = schedule_tasks(tasks, [])
    assert result == ['a', 'b', 'c']

import pytest
from task_scheduler import schedule_tasks

def test_empty_input_returns_empty_output():
    """TP_5: Verify empty input returns empty output."""
    result = schedule_tasks([], [])
    assert result == []

import pytest
from task_scheduler import schedule_tasks

def test_single_task_no_dependencies():
    """TP_6: Verify single task with no dependencies returns that task."""
    result = schedule_tasks(['task1'], [])
    assert result == ['task1']

import pytest
from task_scheduler import schedule_tasks

def test_multiple_independent_tasks_lexicographic():
    """TP_7: Verify multiple independent tasks are returned in lexicographic order."""
    result = schedule_tasks(['b', 'a', 'c'], [])
    assert result == ['a', 'b', 'c']

import pytest
from task_scheduler import schedule_tasks

def test_diamond_shaped_dependency_graph():
    """TP_8: Verify diamond-shaped dependency graph is handled correctly."""
    tasks = ['a', 'b', 'c', 'd']
    dependencies = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd')]
    result = schedule_tasks(tasks, dependencies)
    assert result[0] == 'a'
    assert result[-1] == 'd'
    assert result.index('a') < result.index('b')
    assert result.index('a') < result.index('c')
    assert result.index('b') < result.index('d')
    assert result.index('c') < result.index('d')

import pytest
from task_scheduler import schedule_tasks

def test_multiple_independent_chains():
    """TP_9: Verify multiple independent dependency chains are ordered deterministically."""
    tasks = ['a', 'b', 'c', 'd']
    dependencies = [('a', 'b'), ('c', 'd')]
    result = schedule_tasks(tasks, dependencies)
    assert result.index('a') < result.index('b')
    assert result.index('c') < result.index('d')
    assert len(result) == 4
    assert set(result) == set(tasks)

import pytest
from task_scheduler import schedule_tasks

def test_long_dependency_chain():
    """TP_10: Verify long dependency chain maintains correct order."""
    tasks = ['t1', 't2', 't3', 't4', 't5']
    dependencies = [('t1', 't2'), ('t2', 't3'), ('t3', 't4'), ('t4', 't5')]
    result = schedule_tasks(tasks, dependencies)
    assert result == ['t1', 't2', 't3', 't4', 't5']

import pytest
from task_scheduler import schedule_tasks

def test_duplicate_task_names_raises_valueerror():
    """TP_11: Verify ValueError raised for duplicate task names."""
    with pytest.raises(ValueError, match="[Dd]uplicate"):
        schedule_tasks(['a', 'b', 'a'], [])

import pytest
from task_scheduler import schedule_tasks

def test_unknown_task_in_dependency_raises_valueerror():
    """TP_12: Verify ValueError raised when dependency references unknown task."""
    with pytest.raises(ValueError, match="[Uu]nknown"):
        schedule_tasks(['a', 'b'], [('a', 'c')])

import pytest
from task_scheduler import schedule_tasks

def test_circular_dependency_raises_valueerror():
    """TP_13: Verify ValueError raised for circular dependency."""
    with pytest.raises(ValueError, match="[Cc]ircular"):
        schedule_tasks(['a', 'b'], [('a', 'b'), ('b', 'a')])

import pytest
from task_scheduler import schedule_tasks

def test_self_referential_dependency_raises_valueerror():
    """TP_14: Verify ValueError raised for self-referential dependency."""
    with pytest.raises(ValueError, match="[Cc]ircular"):
        schedule_tasks(['a'], [('a', 'a')])

import pytest
from task_scheduler import schedule_tasks

def test_tasks_not_list_raises_typeerror():
    """TP_15: Verify TypeError raised when tasks parameter is not a list."""
    with pytest.raises(TypeError):
        schedule_tasks('not_a_list', [])

import pytest
from task_scheduler import schedule_tasks

def test_dependencies_not_list_raises_typeerror():
    """TP_16: Verify TypeError raised when dependencies parameter is not a list."""
    with pytest.raises(TypeError):
        schedule_tasks(['a'], 'not_a_list')

import pytest
from task_scheduler import schedule_tasks

def test_task_name_not_string_raises_typeerror():
    """TP_17: Verify TypeError raised when task name is not a string."""
    with pytest.raises(TypeError):
        schedule_tasks(['a', 123], [])

import pytest
from task_scheduler import schedule_tasks

def test_dependency_not_pair_raises_typeerror():
    """TP_18: Verify TypeError raised when dependency is not a pair of strings."""
    with pytest.raises(TypeError):
        schedule_tasks(['a', 'b'], [('a', 'b', 'c')])

import pytest
from task_scheduler import schedule_tasks

def test_dependency_pair_non_string_raises_typeerror():
    """TP_19: Verify TypeError raised when dependency pair contains non-string elements."""
    with pytest.raises(TypeError):
        schedule_tasks(['a', 'b'], [(1, 'b')])

import pytest
from task_scheduler import schedule_tasks

def test_case_sensitive_task_names():
    """TP_20: Verify task names are case-sensitive."""
    result = schedule_tasks(['A', 'a'], [])
    assert len(result) == 2
    assert 'A' in result
    assert 'a' in result
    assert result == ['A', 'a']

import pytest
from task_scheduler import schedule_tasks

def test_no_side_effects():
    """TP_21: Verify function does not execute tasks or modify external state."""
    tasks = ['task1', 'task2']
    dependencies = [('task1', 'task2')]
    result1 = schedule_tasks(tasks, dependencies)
    result2 = schedule_tasks(tasks, dependencies)
    assert result1 == result2
    assert result1 is not result2

import pytest
from task_scheduler import schedule_tasks

def test_deterministic_output_repeated_calls():
    """TP_22: Verify deterministic output on repeated calls with same input."""
    tasks = ['z', 'a', 'm', 'b']
    dependencies = [('z', 'a'), ('m', 'b')]
    results = [schedule_tasks(tasks, dependencies) for _ in range(5)]
    assert all(r == results[0] for r in results)

import pytest
from task_scheduler import schedule_tasks

def test_empty_dependencies_multiple_tasks_lexicographic():
    """TP_23: Verify empty dependencies list with multiple tasks returns lexicographic order."""
    result = schedule_tasks(['z', 'a', 'm'], [])
    assert result == ['a', 'm', 'z']

import pytest
from task_scheduler import schedule_tasks

def test_complex_graph_multiple_dependencies_per_task():
    """TP_24: Verify complex graph with multiple dependencies per task."""
    tasks = ['a', 'b', 'c', 'd', 'e']
    dependencies = [('a', 'c'), ('b', 'c'), ('c', 'd'), ('c', 'e')]
    result = schedule_tasks(tasks, dependencies)
    assert result.index('a') < result.index('c')
    assert result.index('b') < result.index('c')
    assert result.index('c') < result.index('d')
    assert result.index('c') < result.index('e')

import pytest
from task_scheduler import schedule_tasks

def test_unknown_task_in_before_position_raises_valueerror():
    """TP_25: Verify ValueError for dependency referencing unknown task in 'before' position."""
    with pytest.raises(ValueError, match="[Uu]nknown"):
        schedule_tasks(['a', 'b'], [('unknown', 'a')])
