import pytest
from task_scheduler import schedule_tasks

def test_linear_dependency_chain():
    """TP_1: Verify schedule_tasks returns correct ordering for linear dependency chain"""
    tasks = ["fetch_data", "clean_data", "train_model", "evaluate_model"]
    dependencies = [
        ("fetch_data", "clean_data"),
        ("clean_data", "train_model"),
        ("train_model", "evaluate_model")
    ]
    result = schedule_tasks(tasks, dependencies)
    assert result == ["fetch_data", "clean_data", "train_model", "evaluate_model"]
    assert len(result) == len(tasks)
    assert set(result) == set(tasks)

import pytest
from task_scheduler import schedule_tasks

def test_lexicographic_order_no_dependencies():
    """TP_2: Verify schedule_tasks returns lexicographically sorted order when no dependencies exist"""
    tasks = ["b", "a", "c"]
    dependencies = []
    result = schedule_tasks(tasks, dependencies)
    assert result == ["a", "b", "c"]

import pytest
from task_scheduler import schedule_tasks

def test_empty_inputs():
    """TP_3: Verify schedule_tasks returns empty list for empty inputs"""
    tasks = []
    dependencies = []
    result = schedule_tasks(tasks, dependencies)
    assert result == []

import pytest
from task_scheduler import schedule_tasks

def test_single_task():
    """TP_4: Verify schedule_tasks returns single task when only one task provided"""
    tasks = ["task1"]
    dependencies = []
    result = schedule_tasks(tasks, dependencies)
    assert result == ["task1"]

import pytest
from task_scheduler import schedule_tasks

def test_dependency_constraints_respected():
    """TP_5: Verify schedule_tasks respects all dependency constraints in output"""
    tasks = ["a", "b", "c", "d", "e"]
    dependencies = [("a", "b"), ("b", "c"), ("a", "d"), ("d", "e")]
    result = schedule_tasks(tasks, dependencies)
    
    # Check that every dependency is respected
    for before_task, after_task in dependencies:
        before_idx = result.index(before_task)
        after_idx = result.index(after_task)
        assert before_idx < after_idx, f"{before_task} should appear before {after_task}"

import pytest
from task_scheduler import schedule_tasks

def test_deterministic_lexicographic_tiebreaking():
    """TP_6: Verify schedule_tasks returns deterministic output with lexicographic tie-breaking"""
    tasks = ["z", "a", "m", "b"]
    dependencies = []
    
    # Call multiple times to ensure deterministic output
    result1 = schedule_tasks(tasks, dependencies)
    result2 = schedule_tasks(tasks, dependencies)
    result3 = schedule_tasks(tasks, dependencies)
    
    assert result1 == result2 == result3
    assert result1 == ["a", "b", "m", "z"]

import pytest
from task_scheduler import schedule_tasks

def test_diamond_dependency_graph():
    """TP_7: Verify schedule_tasks handles diamond-shaped dependency graph correctly"""
    tasks = ["a", "b", "c", "d"]
    dependencies = [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")]
    result = schedule_tasks(tasks, dependencies)
    
    # Verify a is first and d is last
    assert result[0] == "a"
    assert result[-1] == "d"
    
    # Verify all dependencies are respected
    for before_task, after_task in dependencies:
        before_idx = result.index(before_task)
        after_idx = result.index(after_task)
        assert before_idx < after_idx

import pytest
from task_scheduler import schedule_tasks

def test_multiple_independent_chains():
    """TP_8: Verify schedule_tasks handles multiple independent dependency chains"""
    tasks = ["a", "b", "c", "d", "e", "f"]
    dependencies = [("a", "b"), ("b", "c"), ("d", "e"), ("e", "f")]
    result = schedule_tasks(tasks, dependencies)
    
    # Verify all dependencies are respected
    for before_task, after_task in dependencies:
        before_idx = result.index(before_task)
        after_idx = result.index(after_task)
        assert before_idx < after_idx
    
    # Verify lexicographic ordering is applied
    assert result == ["a", "b", "c", "d", "e", "f"] or result == ["a", "d", "b", "e", "c", "f"]

import pytest
from task_scheduler import schedule_tasks

def test_every_task_appears_exactly_once():
    """TP_9: Verify schedule_tasks includes every task exactly once in output"""
    tasks = ["task1", "task2", "task3", "task4", "task5"]
    dependencies = [("task1", "task2"), ("task3", "task4")]
    result = schedule_tasks(tasks, dependencies)
    
    assert len(result) == len(tasks)
    assert set(result) == set(tasks)
    assert len(result) == len(set(result))  # No duplicates

import pytest
from task_scheduler import schedule_tasks

def test_duplicate_task_names_raises_valueerror():
    """TP_10: Verify schedule_tasks raises ValueError for duplicate task names"""
    tasks = ["task1", "task2", "task1"]
    dependencies = []
    
    with pytest.raises(ValueError, match="Duplicate task names"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_unknown_task_in_dependency_raises_valueerror():
    """TP_11: Verify schedule_tasks raises ValueError for dependency referencing unknown task"""
    tasks = ["task1", "task2"]
    dependencies = [("task1", "unknown_task")]
    
    with pytest.raises(ValueError, match="Dependency refers to unknown task"):
        schedule_tasks(tasks, dependencies)
    
    # Test unknown before_task
    dependencies2 = [("unknown_task", "task1")]
    with pytest.raises(ValueError, match="Dependency refers to unknown task"):
        schedule_tasks(tasks, dependencies2)

import pytest
from task_scheduler import schedule_tasks

def test_circular_dependency_raises_valueerror():
    """TP_12: Verify schedule_tasks raises ValueError for circular dependency"""
    tasks = ["a", "b", "c"]
    dependencies = [("a", "b"), ("b", "c"), ("c", "a")]
    
    with pytest.raises(ValueError, match="Circular dependency exists"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_self_referential_dependency_raises_valueerror():
    """TP_13: Verify schedule_tasks raises ValueError for self-referential dependency"""
    tasks = ["a", "b"]
    dependencies = [("a", "a")]
    
    with pytest.raises(ValueError, match="Circular dependency exists"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_tasks_not_list_raises_typeerror():
    """TP_14: Verify schedule_tasks raises TypeError when tasks parameter is not a list"""
    # Test with tuple
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks(("a", "b"), [])
    
    # Test with dict
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks({"a": 1}, [])
    
    # Test with string
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks("abc", [])
    
    # Test with None
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks(None, [])

import pytest
from task_scheduler import schedule_tasks

def test_dependencies_not_list_raises_typeerror():
    """TP_15: Verify schedule_tasks raises TypeError when dependencies parameter is not a list"""
    tasks = ["a", "b"]
    
    # Test with tuple
    with pytest.raises(TypeError, match="dependencies must be a list"):
        schedule_tasks(tasks, (("a", "b"),))
    
    # Test with dict
    with pytest.raises(TypeError, match="dependencies must be a list"):
        schedule_tasks(tasks, {"a": "b"})
    
    # Test with string
    with pytest.raises(TypeError, match="dependencies must be a list"):
        schedule_tasks(tasks, "ab")
    
    # Test with None
    with pytest.raises(TypeError, match="dependencies must be a list"):
        schedule_tasks(tasks, None)

import pytest
from task_scheduler import schedule_tasks

def test_non_string_task_name_raises_typeerror():
    """TP_16: Verify schedule_tasks raises TypeError when task name is not a string"""
    # Test with integer
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks(["a", 1, "b"], [])
    
    # Test with None
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks(["a", None, "b"], [])
    
    # Test with list
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks(["a", ["b"], "c"], [])

import pytest
from task_scheduler import schedule_tasks

def test_invalid_dependency_format_raises_typeerror():
    """TP_17: Verify schedule_tasks raises TypeError when dependency is not a pair of strings"""
    tasks = ["a", "b", "c"]
    
    # Test with single string
    with pytest.raises(TypeError, match="Dependency must be a pair of strings"):
        schedule_tasks(tasks, ["a"])
    
    # Test with 3-tuple
    with pytest.raises(TypeError, match="Dependency must be a pair of strings"):
        schedule_tasks(tasks, [("a", "b", "c")])
    
    # Test with tuple containing non-strings
    with pytest.raises(TypeError, match="Dependency must be a pair of strings"):
        schedule_tasks(tasks, [("a", 1)])
    
    # Test with tuple containing None
    with pytest.raises(TypeError, match="Dependency must be a pair of strings"):
        schedule_tasks(tasks, [("a", None)])

import pytest
from task_scheduler import schedule_tasks

def test_case_sensitive_task_names():
    """TP_18: Verify schedule_tasks is case-sensitive for task names"""
    tasks = ["Task", "task", "TASK"]
    dependencies = []
    result = schedule_tasks(tasks, dependencies)
    
    # All three should be treated as distinct tasks
    assert len(result) == 3
    assert set(result) == {"Task", "task", "TASK"}
    assert result == ["TASK", "Task", "task"]  # Lexicographic order

import pytest
from task_scheduler import schedule_tasks

def test_no_external_state_modification():
    """TP_19: Verify schedule_tasks does not execute tasks or modify external state"""
    tasks = ["fetch_data", "clean_data", "train_model"]
    dependencies = [("fetch_data", "clean_data"), ("clean_data", "train_model")]
    
    # Store original state
    original_tasks = tasks.copy()
    original_dependencies = dependencies.copy()
    
    # Call the function
    result = schedule_tasks(tasks, dependencies)
    
    # Verify input lists were not modified
    assert tasks == original_tasks
    assert dependencies == original_dependencies
    
    # Verify function only returns ordering
    assert isinstance(result, list)
    assert all(isinstance(task, str) for task in result)

import pytest
from task_scheduler import schedule_tasks

def test_long_dependency_chain():
    """TP_20: Verify schedule_tasks handles long dependency chains efficiently"""
    # Create a long linear chain
    tasks = [f"task_{i}" for i in range(100)]
    dependencies = [(f"task_{i}", f"task_{i+1}") for i in range(99)]
    
    result = schedule_tasks(tasks, dependencies)
    
    # Verify all tasks are included
    assert len(result) == len(tasks)
    assert set(result) == set(tasks)
    
    # Verify the order respects all dependencies
    for before_task, after_task in dependencies:
        before_idx = result.index(before_task)
        after_idx = result.index(after_task)
        assert before_idx < after_idx
