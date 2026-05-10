# Validation Report: task_scheduler_with_dependencies_v1

## Artifact Summary

| Metric | Value |
|---|---:|
| `version` | task_scheduler_with_dependencies_v1 |
| `description_stored` | True |
| `test_plan_items` | 20 |
| `artifact_count` | 5 |
| `generated_code_records` | 1 |
| `generated_test_records` | 20 |
| `test_results` | 20 |
| `tests_passed` | 20 |
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
| section_7, section_8, section_9 | `TP_1` | Verify schedule_tasks returns correct ordering for linear dependency chain | `test_linear_dependency_chain` | passed |
| section_1.2 | `TP_2` | Verify schedule_tasks returns lexicographically sorted order when no dependencies exist | `test_lexicographic_order_no_dependencies` | passed |
| section_1.4 | `TP_3` | Verify schedule_tasks returns empty list for empty inputs | `test_empty_inputs` | passed |
| section_1.4 | `TP_4` | Verify schedule_tasks returns single task when only one task provided | `test_single_task` | passed |
| section_1.2 | `TP_5` | Verify schedule_tasks respects all dependency constraints in output | `test_dependency_constraints_respected` | passed |
| section_1.2 | `TP_6` | Verify schedule_tasks returns deterministic output with lexicographic tie-breaking | `test_deterministic_lexicographic_tiebreaking` | passed |
| section_1.4, section_14, section_15 | `TP_7` | Verify schedule_tasks handles diamond-shaped dependency graph correctly | `test_diamond_dependency_graph` | passed |
| section_1.4 | `TP_8` | Verify schedule_tasks handles multiple independent dependency chains | `test_multiple_independent_chains` | passed |
| section_1.2 | `TP_9` | Verify schedule_tasks includes every task exactly once in output | `test_every_task_appears_exactly_once` | passed |
| section_1.3, section_10, section_11 | `TP_10` | Verify schedule_tasks raises ValueError for duplicate task names | `test_duplicate_task_names_raises_valueerror` | passed |
| section_1.3, section_10, section_11 | `TP_11` | Verify schedule_tasks raises ValueError for dependency referencing unknown task | `test_unknown_task_in_dependency_raises_valueerror` | passed |
| section_1.3, section_10, section_11 | `TP_12` | Verify schedule_tasks raises ValueError for circular dependency | `test_circular_dependency_raises_valueerror` | passed |
| section_1.3, section_10, section_11 | `TP_13` | Verify schedule_tasks raises ValueError for self-referential dependency | `test_self_referential_dependency_raises_valueerror` | passed |
| section_1.3, section_10, section_11 | `TP_14` | Verify schedule_tasks raises TypeError when tasks parameter is not a list | `test_tasks_not_list_raises_typeerror` | passed |
| section_1.3, section_10, section_11 | `TP_15` | Verify schedule_tasks raises TypeError when dependencies parameter is not a list | `test_dependencies_not_list_raises_typeerror` | passed |
| section_1.3, section_10, section_11 | `TP_16` | Verify schedule_tasks raises TypeError when task name is not a string | `test_non_string_task_name_raises_typeerror` | passed |
| section_1.3, section_10, section_11 | `TP_17` | Verify schedule_tasks raises TypeError when dependency is not a pair of strings | `test_invalid_dependency_format_raises_typeerror` | passed |
| section_1.5 | `TP_18` | Verify schedule_tasks is case-sensitive for task names | `test_case_sensitive_task_names` | passed |
| section_1.5 | `TP_19` | Verify schedule_tasks does not execute tasks or modify external state | `test_no_external_state_modification` | passed |
| section_1.4 | `TP_20` | Verify schedule_tasks handles long dependency chains efficiently | `test_long_dependency_chain` | passed |

## Overall Result

Passed with 3 warning(s).
