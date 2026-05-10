# Validation Report: task_scheduler_with_dependencies_v1

## Artifact Summary

| Metric | Value |
|---|---:|
| `version` | task_scheduler_with_dependencies_v1 |
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
| section_1.1 | `TP_1` | Verify function signature matches schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) -> list[str] | `test_function_signature` | passed |
| section_7, section_8, section_9 | `TP_2` | Test basic linear dependency chain execution order | `test_basic_linear_dependency_chain` | passed |
| section_1.2 | `TP_3` | Verify every task in input appears exactly once in output | `test_all_tasks_appear_exactly_once` | passed |
| section_1.2 | `TP_4` | Verify dependency ordering constraint: for each (A, B) pair, A appears before B | `test_dependency_ordering_constraint` | passed |
| section_1.2 | `TP_5` | Test lexicographic ordering when multiple tasks are available | `test_lexicographic_ordering_no_dependencies` | passed |
| section_1.2 | `TP_6` | Test deterministic output consistency across multiple calls | `test_deterministic_output_consistency` | passed |
| section_1.4, section_12, section_13 | `TP_7` | Test empty tasks and dependencies boundary condition | `test_empty_tasks_and_dependencies` | passed |
| section_1.4, section_12, section_13 | `TP_8` | Test single task with no dependencies boundary condition | `test_single_task_no_dependencies` | passed |
| section_1.4, section_12, section_13 | `TP_9` | Test multiple independent tasks with no dependencies | `test_multiple_independent_tasks` | passed |
| section_1.4, section_12, section_13 | `TP_10` | Test long linear dependency chain | `test_long_linear_dependency_chain` | passed |
| section_1.4, section_14, section_15 | `TP_11` | Test diamond-shaped dependency graph | `test_diamond_shaped_dependency_graph` | passed |
| section_1.4, section_12, section_13 | `TP_12` | Test multiple independent dependency chains | `test_multiple_independent_chains` | passed |
| section_1.3, section_10, section_11 | `TP_13` | Test ValueError for duplicate task names | `test_duplicate_task_names_error` | passed |
| section_1.3, section_10, section_11 | `TP_14` | Test ValueError for dependency referring to unknown task | `test_unknown_task_in_dependency_error` | passed |
| section_1.3, section_10, section_11 | `TP_15` | Test ValueError for circular dependency | `test_circular_dependency_error` | passed |
| section_1.3, section_10, section_11 | `TP_16` | Test TypeError when tasks parameter is not a list | `test_tasks_not_list_error` | passed |
| section_1.3, section_10, section_11 | `TP_17` | Test TypeError when dependencies parameter is not a list | `test_dependencies_not_list_error` | passed |
| section_1.3, section_10, section_11 | `TP_18` | Test TypeError when task name is not a string | `test_task_name_not_string_error` | passed |
| section_1.3, section_10, section_11 | `TP_19` | Test TypeError when dependency is not a pair of strings | `test_dependency_not_pair_of_strings_error` | passed |
| section_1.5 | `TP_20` | Verify task names are case-sensitive | `test_case_sensitive_task_names` | passed |
| section_1.5 | `TP_21` | Verify function returns ordering only without executing tasks | `test_function_returns_ordering_only` | passed |
| section_1.2, section_1.4 | `TP_22` | Test complex graph with multiple paths and convergence points | `test_complex_graph_multiple_paths` | passed |
| section_1.3, section_10, section_11 | `TP_23` | Test self-dependency error handling | `test_self_dependency_error` | passed |
| section_1.4, section_12, section_13 | `TP_24` | Test empty dependencies list with multiple tasks | `test_empty_dependencies_multiple_tasks` | passed |
| section_1.5 | `TP_25` | Test large number of tasks and dependencies for performance | `test_large_number_of_tasks_performance` | passed |

## Overall Result

Passed with 3 warning(s).
