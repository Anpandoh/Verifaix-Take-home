# Validation Report: task_scheduler_with_v1

## Artifact Summary

| Metric | Value |
|---|---:|
| `version` | task_scheduler_with_v1 |
| `description_stored` | True |
| `test_plan_items` | 25 |
| `artifact_count` | 4 |
| `generated_code_records` | 1 |
| `generated_test_records` | 25 |
| `test_results` | 25 |
| `tests_passed` | 25 |
| `tests_failed` | 0 |

## Generated Program Summary

Module: `task_scheduler`

schedule_tasks(tasks, dependencies): Computes a valid execution order for tasks with dependencies. It raises TypeError, ValueError for error cases.

| Function | Parameters | Returns | Raises |
|---|---|---|---|
| `schedule_tasks` | `tasks`, `dependencies` | _missing_ | `TypeError`, `ValueError` |

## Static Checks

| Severity | Check | Message |
|---|---|---|
| warning | `generated_code_annotations` | schedule_tasks is missing argument or return type annotations. |
| warning | `generated_tests_duplicate_imports` | Generated tests repeat imports: pytest, task_scheduler:schedule_tasks. |
| warning | `generated_tests_import_order` | Generated tests contain imports after test functions. |

## Delta Summary

No deltas are stored for this version.


## Traceability Matrix

| Source Sections | Test Plan ID | Requirement | Test Functions | Results |
|---|---|---|---|---|
| section_1.1 | `TP_1` | Verify schedule_tasks function exists with correct signature accepting tasks list and dependencies list | `test_function_exists_with_correct_signature` | passed |
| section_1.2 | `TP_2` | Verify function returns all tasks exactly once in output | `test_returns_all_tasks_exactly_once` | passed |
| section_1.2, section_7 | `TP_3` | Verify dependency ordering is respected for simple linear chain | `test_simple_linear_dependency_chain` | passed |
| section_1.2 | `TP_4` | Verify lexicographic ordering when multiple tasks are available | `test_lexicographic_ordering_no_dependencies` | passed |
| section_1.4 | `TP_5` | Verify empty input returns empty output | `test_empty_input_returns_empty_output` | passed |
| section_1.4 | `TP_6` | Verify single task with no dependencies returns that task | `test_single_task_no_dependencies` | passed |
| section_1.4 | `TP_7` | Verify multiple independent tasks are returned in lexicographic order | `test_multiple_independent_tasks_lexicographic` | passed |
| section_1.4, section_14 | `TP_8` | Verify diamond-shaped dependency graph is handled correctly | `test_diamond_shaped_dependency_graph` | passed |
| section_1.4 | `TP_9` | Verify multiple independent dependency chains are ordered deterministically | `test_multiple_independent_chains` | passed |
| section_1.4 | `TP_10` | Verify long dependency chain maintains correct order | `test_long_dependency_chain` | passed |
| section_1.3 | `TP_11` | Verify ValueError raised for duplicate task names | `test_duplicate_task_names_raises_valueerror` | passed |
| section_1.3 | `TP_12` | Verify ValueError raised when dependency references unknown task | `test_unknown_task_in_dependency_raises_valueerror` | passed |
| section_1.3 | `TP_13` | Verify ValueError raised for circular dependency | `test_circular_dependency_raises_valueerror` | passed |
| section_1.3 | `TP_14` | Verify ValueError raised for self-referential dependency | `test_self_referential_dependency_raises_valueerror` | passed |
| section_1.3 | `TP_15` | Verify TypeError raised when tasks parameter is not a list | `test_tasks_not_list_raises_typeerror` | passed |
| section_1.3 | `TP_16` | Verify TypeError raised when dependencies parameter is not a list | `test_dependencies_not_list_raises_typeerror` | passed |
| section_1.3 | `TP_17` | Verify TypeError raised when task name is not a string | `test_task_name_not_string_raises_typeerror` | passed |
| section_1.3 | `TP_18` | Verify TypeError raised when dependency is not a pair of strings | `test_dependency_not_pair_raises_typeerror` | passed |
| section_1.3 | `TP_19` | Verify TypeError raised when dependency pair contains non-string elements | `test_dependency_pair_non_string_raises_typeerror` | passed |
| section_1.5 | `TP_20` | Verify task names are case-sensitive | `test_case_sensitive_task_names` | passed |
| section_1.5 | `TP_21` | Verify function does not execute tasks or modify external state | `test_no_side_effects` | passed |
| section_1.2, section_1.5 | `TP_22` | Verify deterministic output on repeated calls with same input | `test_deterministic_output_repeated_calls` | passed |
| section_1.4 | `TP_23` | Verify empty dependencies list with multiple tasks returns lexicographic order | `test_empty_dependencies_multiple_tasks_lexicographic` | passed |
| section_1.2 | `TP_24` | Verify complex graph with multiple dependencies per task | `test_complex_graph_multiple_dependencies_per_task` | passed |
| section_1.3 | `TP_25` | Verify ValueError for dependency referencing unknown task in 'before' position | `test_unknown_task_in_before_position_raises_valueerror` | passed |

## Overall Result

Passed with 3 warning(s).
