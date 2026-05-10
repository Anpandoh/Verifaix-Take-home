import pytest
from task_scheduler import schedule_tasks

def test_linear_dependency_chain():
    """
    TP_1: Verify schedule_tasks returns correct ordering for linear dependency chain
    """
    tasks = ["fetch_data", "clean_data", "train_model", "evaluate_model"]
    dependencies = [
        ("fetch_data", "clean_data"),
        ("clean_data", "train_model"),
        ("train_model", "evaluate_model")
    ]
    result = schedule_tasks(tasks, dependencies)
    assert result == ["fetch_data", "clean_data", "train_model", "evaluate_model"]

import pytest
from task_scheduler import schedule_tasks

def test_lexicographic_ordering_no_dependencies():
    """
    TP_2: Verify lexicographic ordering when no dependencies exist
    """
    tasks = ["b", "a", "c"]
    dependencies = []
    result = schedule_tasks(tasks, dependencies)
    assert result == ["c", "b", "a"]

import pytest
from task_scheduler import schedule_tasks

def test_all_tasks_appear_exactly_once():
    """
    TP_3: Verify every task appears exactly once in output
    """
    tasks = ["task1", "task2", "task3", "task4", "task5"]
    dependencies = [("task1", "task2"), ("task3", "task4")]
    result = schedule_tasks(tasks, dependencies)
    assert len(result) == len(tasks)
    assert set(result) == set(tasks)
    assert len(result) == len(set(result))

import pytest
from task_scheduler import schedule_tasks

def test_dependency_ordering_constraint():
    """
    TP_4: Verify dependency ordering constraint is satisfied
    """
    tasks = ["a", "b", "c", "d", "e"]
    dependencies = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e")]
    result = schedule_tasks(tasks, dependencies)
    for before_task, after_task in dependencies:
        before_idx = result.index(before_task)
        after_idx = result.index(after_task)
        assert before_idx < after_idx

import pytest
from task_scheduler import schedule_tasks

def test_deterministic_output():
    """
    TP_5: Verify deterministic output on multiple valid orderings
    """
    tasks = ["x", "y", "z"]
    dependencies = []
    result1 = schedule_tasks(tasks, dependencies)
    result2 = schedule_tasks(tasks, dependencies)
    result3 = schedule_tasks(tasks, dependencies)
    assert result1 == result2 == result3

import pytest
from task_scheduler import schedule_tasks

def test_diamond_dependency_graph():
    """
    TP_6: Verify diamond-shaped dependency graph handling
    """
    tasks = ["a", "b", "c", "d"]
    dependencies = [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")]
    result = schedule_tasks(tasks, dependencies)
    assert result.index("a") < result.index("b")
    assert result.index("a") < result.index("c")
    assert result.index("b") < result.index("d")
    assert result.index("c") < result.index("d")

import pytest
from task_scheduler import schedule_tasks

def test_multiple_independent_chains():
    """
    TP_7: Verify multiple independent dependency chains
    """
    tasks = ["a", "b", "c", "d", "e", "f"]
    dependencies = [("a", "b"), ("b", "c"), ("d", "e"), ("e", "f")]
    result = schedule_tasks(tasks, dependencies)
    assert result.index("a") < result.index("b")
    assert result.index("b") < result.index("c")
    assert result.index("d") < result.index("e")
    assert result.index("e") < result.index("f")
    assert len(result) == 6
    assert set(result) == set(tasks)

import pytest
from task_scheduler import schedule_tasks

def test_empty_input():
    """
    TP_8: Verify empty input returns empty list
    """
    tasks = []
    dependencies = []
    result = schedule_tasks(tasks, dependencies)
    assert result == []

import pytest
from task_scheduler import schedule_tasks

def test_single_task_no_dependencies():
    """
    TP_9: Verify single task with no dependencies
    """
    tasks = ["only_task"]
    dependencies = []
    result = schedule_tasks(tasks, dependencies)
    assert result == ["only_task"]

import pytest
from task_scheduler import schedule_tasks

def test_long_dependency_chain():
    """
    TP_10: Verify long dependency chain execution
    """
    tasks = [f"task_{i}" for i in range(20)]
    dependencies = [(f"task_{i}", f"task_{i+1}") for i in range(19)]
    result = schedule_tasks(tasks, dependencies)
    assert len(result) == 20
    for i in range(19):
        assert result.index(f"task_{i}") < result.index(f"task_{i+1}")

import pytest
from task_scheduler import schedule_tasks

def test_duplicate_task_names_raises_valueerror():
    """
    TP_11: Verify ValueError on duplicate task names
    """
    tasks = ["task1", "task2", "task1"]
    dependencies = []
    with pytest.raises(ValueError):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_unknown_task_in_dependency_raises_valueerror():
    """
    TP_12: Verify ValueError on unknown task in dependency
    """
    tasks = ["task1", "task2"]
    dependencies = [("task1", "unknown_task")]
    with pytest.raises(ValueError):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_circular_dependency_raises_valueerror():
    """
    TP_13: Verify ValueError on circular dependency
    """
    tasks = ["a", "b", "c"]
    dependencies = [("a", "b"), ("b", "c"), ("c", "a")]
    with pytest.raises(ValueError):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_tasks_not_list_raises_typeerror():
    """
    TP_14: Verify TypeError when tasks is not a list
    """
    with pytest.raises(TypeError):
        schedule_tasks(("task1", "task2"), [])
    with pytest.raises(TypeError):
        schedule_tasks("task1", [])
    with pytest.raises(TypeError):
        schedule_tasks({"task1": 1}, [])

import pytest
from task_scheduler import schedule_tasks

def test_dependencies_not_list_raises_typeerror():
    """
    TP_15: Verify TypeError when dependencies is not a list
    """
    tasks = ["task1", "task2"]
    with pytest.raises(TypeError):
        schedule_tasks(tasks, ("task1", "task2"))
    with pytest.raises(TypeError):
        schedule_tasks(tasks, "dependency")

import pytest
from task_scheduler import schedule_tasks

def test_task_name_not_string_raises_typeerror():
    """
    TP_16: Verify TypeError when task name is not a string
    """
    with pytest.raises(TypeError):
        schedule_tasks(["task1", 123], [])
    with pytest.raises(TypeError):
        schedule_tasks(["task1", None], [])
    with pytest.raises(TypeError):
        schedule_tasks(["task1", ["nested"]], [])

import pytest
from task_scheduler import schedule_tasks

def test_dependency_not_pair_of_strings_raises_typeerror():
    """
    TP_17: Verify TypeError when dependency is not a pair of strings
    """
    tasks = ["task1", "task2"]
    with pytest.raises(TypeError):
        schedule_tasks(tasks, [("task1",)])
    with pytest.raises(TypeError):
        schedule_tasks(tasks, [("task1", "task2", "task3")])
    with pytest.raises(TypeError):
        schedule_tasks(tasks, [("task1", 123)])
    with pytest.raises(TypeError):
        schedule_tasks(tasks, [(123, "task2")])

import pytest
from task_scheduler import schedule_tasks

def test_case_sensitive_task_names():
    """
    TP_18: Verify case-sensitive task name handling
    """
    tasks = ["Task", "task", "TASK"]
    dependencies = [("Task", "task"), ("task", "TASK")]
    result = schedule_tasks(tasks, dependencies)
    assert result.index("Task") < result.index("task")
    assert result.index("task") < result.index("TASK")
    assert len(result) == 3

import pytest
from task_scheduler import schedule_tasks

def test_no_side_effects():
    """
    TP_19: Verify function does not execute tasks or modify external state
    """
    tasks = ["task1", "task2", "task3"]
    dependencies = [("task1", "task2"), ("task2", "task3")]
    tasks_copy = tasks.copy()
    dependencies_copy = dependencies.copy()
    result = schedule_tasks(tasks, dependencies)
    assert tasks == tasks_copy
    assert dependencies == dependencies_copy
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)

import pytest
from task_scheduler import schedule_tasks

def test_self_referential_dependency_raises_valueerror():
    """
    TP_20: Verify self-referential dependency is rejected
    """
    tasks = ["task1", "task2"]
    dependencies = [("task1", "task1")]
    with pytest.raises(ValueError):
        schedule_tasks(tasks, dependencies)
