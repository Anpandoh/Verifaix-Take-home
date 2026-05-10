import pytest
from task_scheduler import schedule_tasks

def test_function_signature_api_specification():
    """TP_1: Verify function signature matches API specification."""
    # Test that function accepts list[str] tasks and list[tuple[str, str]] dependencies
    tasks = ["task1", "task2"]
    dependencies = [("task1", "task2")]
    result = schedule_tasks(tasks, dependencies)
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)

import pytest
from task_scheduler import schedule_tasks

def test_linear_dependency_chain_execution_order():
    """TP_2: Test linear dependency chain execution order."""
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
    """TP_3: Test lexicographic ordering when no dependencies exist."""
    tasks = ["b", "a", "c"]
    dependencies = []
    result = schedule_tasks(tasks, dependencies)
    assert result == ["c", "b", "a"]

import pytest
from task_scheduler import schedule_tasks

def test_single_task_no_dependencies():
    """TP_4: Test single task with no dependencies."""
    tasks = ["single_task"]
    dependencies = []
    result = schedule_tasks(tasks, dependencies)
    assert result == ["single_task"]

import pytest
from task_scheduler import schedule_tasks

def test_empty_tasks_and_dependencies():
    """TP_5: Test empty tasks and dependencies."""
    tasks = []
    dependencies = []
    result = schedule_tasks(tasks, dependencies)
    assert result == []

import pytest
from task_scheduler import schedule_tasks

def test_diamond_shaped_dependency_graph():
    """TP_6: Test diamond-shaped dependency graph."""
    tasks = ["a", "b", "c", "d"]
    dependencies = [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")]
    result = schedule_tasks(tasks, dependencies)
    # Verify a comes before b and c
    assert result.index("a") < result.index("b")
    assert result.index("a") < result.index("c")
    # Verify b and c come before d
    assert result.index("b") < result.index("d")
    assert result.index("c") < result.index("d")
    # Verify all tasks are present
    assert set(result) == {"a", "b", "c", "d"}

import pytest
from task_scheduler import schedule_tasks

def test_multiple_independent_dependency_chains():
    """TP_7: Test multiple independent dependency chains."""
    tasks = ["a1", "a2", "b1", "b2"]
    dependencies = [("a1", "a2"), ("b1", "b2")]
    result = schedule_tasks(tasks, dependencies)
    # Verify chain a1 -> a2
    assert result.index("a1") < result.index("a2")
    # Verify chain b1 -> b2
    assert result.index("b1") < result.index("b2")
    # Verify all tasks are present
    assert set(result) == {"a1", "a2", "b1", "b2"}
    # Verify deterministic ordering (lexicographic for available tasks)
    result2 = schedule_tasks(tasks, dependencies)
    assert result == result2

import pytest
from task_scheduler import schedule_tasks

def test_duplicate_task_names_raises_valueerror():
    """TP_8: Test duplicate task names raises ValueError."""
    tasks = ["task1", "task2", "task1"]
    dependencies = []
    with pytest.raises(ValueError, match="Duplicate task names"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_dependency_references_unknown_task_raises_valueerror():
    """TP_9: Test dependency references unknown task raises ValueError."""
    tasks = ["task1", "task2"]
    dependencies = [("task1", "unknown_task")]
    with pytest.raises(ValueError, match="unknown task"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_circular_dependency_raises_valueerror():
    """TP_10: Test circular dependency raises ValueError."""
    tasks = ["a", "b", "c"]
    dependencies = [("a", "b"), ("b", "c"), ("c", "a")]
    with pytest.raises(ValueError, match="Circular dependency"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_tasks_parameter_not_list_raises_typeerror():
    """TP_11: Test tasks parameter is not a list raises TypeError."""
    tasks = "not_a_list"
    dependencies = []
    with pytest.raises(TypeError, match="tasks must be a list"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_dependencies_parameter_not_list_raises_typeerror():
    """TP_12: Test dependencies parameter is not a list raises TypeError."""
    tasks = ["task1", "task2"]
    dependencies = "not_a_list"
    with pytest.raises(TypeError, match="dependencies must be a list"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_task_name_not_string_raises_typeerror():
    """TP_13: Test task name is not a string raises TypeError."""
    tasks = ["task1", 123, "task3"]
    dependencies = []
    with pytest.raises(TypeError, match="Task name must be a string"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_dependency_pair_not_tuple_of_strings_raises_typeerror():
    """TP_14: Test dependency pair is not a tuple of strings raises TypeError."""
    tasks = ["task1", "task2"]
    dependencies = [("task1", 123)]
    with pytest.raises(TypeError, match="Dependency must be a pair of strings"):
        schedule_tasks(tasks, dependencies)

import pytest
from task_scheduler import schedule_tasks

def test_case_sensitivity_of_task_names():
    """TP_15: Test case sensitivity of task names."""
    tasks = ["Task", "task", "TASK"]
    dependencies = [("Task", "task"), ("task", "TASK")]
    result = schedule_tasks(tasks, dependencies)
    # Verify case-sensitive ordering
    assert result.index("Task") < result.index("task")
    assert result.index("task") < result.index("TASK")
    assert set(result) == {"Task", "task", "TASK"}

import pytest
from task_scheduler import schedule_tasks

def test_function_does_not_execute_tasks_or_modify_state():
    """TP_16: Test function does not execute tasks or modify external state."""
    # This test verifies the function returns ordering only
    tasks = ["task1", "task2", "task3"]
    dependencies = [("task1", "task2"), ("task2", "task3")]
    result = schedule_tasks(tasks, dependencies)
    # Verify result is just an ordering (list of strings)
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)
    # Verify no side effects by calling again
    result2 = schedule_tasks(tasks, dependencies)
    assert result == result2

import pytest
from task_scheduler import schedule_tasks

def test_every_task_appears_exactly_once_in_output():
    """TP_17: Test every task appears exactly once in output."""
    tasks = ["a", "b", "c", "d", "e"]
    dependencies = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "e")]
    result = schedule_tasks(tasks, dependencies)
    # Verify all tasks are present
    assert set(result) == set(tasks)
    # Verify each task appears exactly once
    assert len(result) == len(tasks)
    assert len(set(result)) == len(result)

import pytest
from task_scheduler import schedule_tasks

def test_deterministic_output_on_repeated_calls():
    """TP_18: Test deterministic output on repeated calls."""
    tasks = ["z", "y", "x", "w"]
    dependencies = [("z", "y"), ("x", "w")]
    result1 = schedule_tasks(tasks, dependencies)
    result2 = schedule_tasks(tasks, dependencies)
    result3 = schedule_tasks(tasks, dependencies)
    assert result1 == result2
    assert result2 == result3

import pytest
from task_scheduler import schedule_tasks

def test_long_dependency_chain_with_many_tasks():
    """TP_19: Test long dependency chain with many tasks."""
    tasks = [f"task_{i}" for i in range(20)]
    dependencies = [(f"task_{i}", f"task_{i+1}") for i in range(19)]
    result = schedule_tasks(tasks, dependencies)
    # Verify all tasks are present
    assert set(result) == set(tasks)
    # Verify dependency order is maintained
    for i in range(19):
        assert result.index(f"task_{i}") < result.index(f"task_{i+1}")

import pytest
from task_scheduler import schedule_tasks

def test_complex_graph_with_multiple_paths_and_convergence():
    """TP_20: Test complex graph with multiple paths and convergence points."""
    tasks = ["start", "path1a", "path1b", "path2a", "path2b", "merge", "end"]
    dependencies = [
        ("start", "path1a"),
        ("start", "path2a"),
        ("path1a", "path1b"),
        ("path2a", "path2b"),
        ("path1b", "merge"),
        ("path2b", "merge"),
        ("merge", "end")
    ]
    result = schedule_tasks(tasks, dependencies)
    # Verify all tasks are present
    assert set(result) == set(tasks)
    # Verify start comes first
    assert result[0] == "start"
    # Verify end comes last
    assert result[-1] == "end"
    # Verify merge comes after both path1b and path2b
    assert result.index("path1b") < result.index("merge")
    assert result.index("path2b") < result.index("merge")
    # Verify all dependencies are respected
    assert result.index("start") < result.index("path1a")
    assert result.index("start") < result.index("path2a")
    assert result.index("path1a") < result.index("path1b")
    assert result.index("path2a") < result.index("path2b")
    assert result.index("merge") < result.index("end")
