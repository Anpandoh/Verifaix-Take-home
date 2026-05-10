# Validation Report: task_scheduler_with_dependencies_v1

## Artifact Summary

| Metric | Value |
|---|---:|
| `version` | task_scheduler_with_dependencies_v1 |
| `description_stored` | True |
| `test_plan_items` | 24 |
| `artifact_count` | 4 |
| `generated_code_records` | 1 |
| `generated_test_records` | 24 |
| `test_results` | 48 |
| `tests_passed` | 46 |
| `tests_failed` | 2 |

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
| error | `test_result_passed` | test_dependency_not_pair_of_strings_raises_typeerror ended with status failed. |
| error | `test_result_passed` | test_dependency_not_pair_of_strings_raises_typeerror ended with status failed. |

## Delta Summary

No deltas are stored for this version.


## Traceability Matrix

| Source Sections | Test Plan ID | Requirement | Test Functions | Results |
|---|---|---|---|---|
| section_1.1 | `TP_1` | Verify function signature matches schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) -> list[str] | `test_function_signature` | passed |
| section_7, section_8, section_9 | `TP_2` | Verify basic linear dependency chain execution order | `test_basic_linear_dependency_chain` | passed |
| section_1.2 | `TP_3` | Verify lexicographic ordering when no dependencies exist | `test_lexicographic_ordering_no_dependencies` | passed |
| section_1.2 | `TP_4` | Verify every task appears exactly once in output | `test_all_tasks_appear_exactly_once` | passed |
| section_1.2 | `TP_5` | Verify dependency ordering constraint is satisfied | `test_dependency_ordering_constraint` | passed |
| section_1.2 | `TP_6` | Verify deterministic output with lexicographic selection | `test_deterministic_lexicographic_selection` | passed |
| section_14, section_15 | `TP_7` | Verify diamond-shaped dependency graph handling | `test_diamond_dependency_graph` | passed |
| section_1.4 | `TP_8` | Verify empty tasks and dependencies returns empty list | `test_empty_tasks_and_dependencies` | passed |
| section_1.4 | `TP_9` | Verify single task with no dependencies | `test_single_task_no_dependencies` | passed |
| section_1.4 | `TP_10` | Verify multiple independent chains are ordered deterministically | `test_multiple_independent_chains` | passed |
| section_1.4 | `TP_11` | Verify long dependency chain execution | `test_long_dependency_chain` | passed |
| section_10, section_11 | `TP_12` | Verify ValueError on duplicate task names | `test_duplicate_task_names_raises_valueerror` | passed |
| section_10, section_11 | `TP_13` | Verify ValueError on dependency referring to unknown task | `test_unknown_task_in_dependency_raises_valueerror` | passed |
| section_10, section_11 | `TP_14` | Verify ValueError on circular dependency detection | `test_circular_dependency_raises_valueerror` | passed |
| section_10, section_11 | `TP_15` | Verify TypeError when tasks parameter is not a list | `test_tasks_not_list_raises_typeerror` | passed |
| section_10, section_11 | `TP_16` | Verify TypeError when dependencies parameter is not a list | `test_dependencies_not_list_raises_typeerror` | passed |
| section_10, section_11 | `TP_17` | Verify TypeError when task name is not a string | `test_task_name_not_string_raises_typeerror` | passed |
| section_10, section_11 | `TP_18` | Verify TypeError when dependency is not a pair of strings | `test_dependency_not_pair_of_strings_raises_typeerror` | failed |
| section_1.5 | `TP_19` | Verify task names are case-sensitive | `test_case_sensitive_task_names` | passed |
| section_1.5 | `TP_20` | Verify function does not execute tasks or modify external state | `test_function_does_not_execute_tasks` | passed |
| section_10, section_11 | `TP_21` | Verify self-referential dependency is rejected | `test_self_referential_dependency_raises_valueerror` | passed |
| section_1.2 | `TP_22` | Verify complex multi-level dependency graph | `test_complex_multi_level_dependency_graph` | passed |
| section_1.4 | `TP_23` | Verify empty dependencies list with multiple tasks | `test_empty_dependencies_multiple_tasks` | passed |
| section_1.2 | `TP_24` | Verify duplicate dependencies are handled correctly | `test_duplicate_dependencies_handled_correctly` | passed |

## Overall Result

Failed validation with 2 error(s) and 3 warning(s).
