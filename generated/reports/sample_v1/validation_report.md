# Validation Report: sample_v1

## Artifact Summary

| Metric | Value |
|---|---:|
| `version` | sample_v1 |
| `description_stored` | True |
| `test_plan_items` | 25 |
| `artifact_count` | 4 |
| `generated_code_records` | 1 |
| `generated_test_records` | 25 |
| `test_results` | 75 |
| `tests_passed` | 75 |
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
| section_2, section_1.1 | `TP_1` | Verify function signature matches schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) -> list[str] | `test_function_signature` | passed |
| section_7, section_8, section_9 | `TP_2` | Verify basic linear dependency chain is ordered correctly | `test_basic_linear_dependency_chain` | passed |
| section_1.2 | `TP_3` | Verify every task in input appears exactly once in output | `test_all_tasks_appear_exactly_once` | passed |
| section_1.2 | `TP_4` | Verify dependency ordering constraint: for each (A, B) pair, A appears before B | `test_dependency_ordering_constraint` | passed |
| section_1.2 | `TP_5` | Verify lexicographic ordering when multiple tasks are available | `test_lexicographic_ordering_no_dependencies` | passed |
| section_1.2 | `TP_6` | Verify deterministic output across multiple invocations | `test_deterministic_output` | passed |
| section_1.4, section_12, section_13 | `TP_7` | Verify empty input returns empty output | `test_empty_input` | passed |
| section_1.4, section_12, section_13 | `TP_8` | Verify single task with no dependencies returns that task | `test_single_task_no_dependencies` | passed |
| section_1.4, section_12, section_13 | `TP_9` | Verify multiple independent tasks return lexicographic order | `test_multiple_independent_tasks_lexicographic` | passed |
| section_1.4, section_12, section_13 | `TP_10` | Verify long linear dependency chain maintains order | `test_long_linear_dependency_chain` | passed |
| section_1.4, section_14, section_15 | `TP_11` | Verify diamond-shaped dependency graph resolves correctly | `test_diamond_dependency_graph` | passed |
| section_1.4, section_12, section_13 | `TP_12` | Verify multiple independent chains with lexicographic tie-breaking | `test_multiple_independent_chains` | passed |
| section_1.3, section_10, section_11 | `TP_13` | Verify ValueError raised for duplicate task names | `test_duplicate_task_names_raises_valueerror` | passed |
| section_1.3, section_10, section_11 | `TP_14` | Verify ValueError raised when dependency references unknown task | `test_unknown_task_in_dependency_raises_valueerror` | passed |
| section_1.3, section_10, section_11 | `TP_15` | Verify ValueError raised for circular dependency | `test_circular_dependency_raises_valueerror` | passed |
| section_1.3, section_10, section_11 | `TP_16` | Verify TypeError raised when tasks parameter is not a list | `test_tasks_not_list_raises_typeerror` | passed |
| section_1.3, section_10, section_11 | `TP_17` | Verify TypeError raised when dependencies parameter is not a list | `test_dependencies_not_list_raises_typeerror` | passed |
| section_1.3, section_10, section_11 | `TP_18` | Verify TypeError raised when task name is not a string | `test_task_name_not_string_raises_typeerror` | passed |
| section_1.3, section_10, section_11 | `TP_19` | Verify TypeError raised when dependency is not a pair of strings | `test_dependency_not_pair_of_strings_raises_typeerror` | passed |
| section_1.5 | `TP_20` | Verify task names are case-sensitive | `test_case_sensitive_task_names` | passed |
| section_1.5 | `TP_21` | Verify function returns ordering only without executing tasks | `test_function_returns_ordering_only` | passed |
| section_1.3, section_10, section_11 | `TP_22` | Verify self-dependency is detected as circular | `test_self_dependency_raises_valueerror` | passed |
| section_1.2 | `TP_23` | Verify complex multi-level dependency graph | `test_complex_multi_level_dependency_graph` | passed |
| section_1.4, section_12, section_13 | `TP_24` | Verify empty dependencies list with multiple tasks | `test_empty_dependencies_multiple_tasks` | passed |
| section_1.5 | `TP_25` | Verify performance with large task count | `test_large_task_count_performance` | passed |

## Overall Result

Passed with 3 warning(s).
