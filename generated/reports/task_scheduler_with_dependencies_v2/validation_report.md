# Validation Report: task_scheduler_with_dependencies_v2

## Artifact Summary

| Metric | Value |
|---|---:|
| `version` | task_scheduler_with_dependencies_v2 |
| `description_stored` | True |
| `test_plan_items` | 24 |
| `artifact_count` | 4 |
| `generated_code_records` | 1 |
| `generated_test_records` | 24 |
| `test_results` | 24 |
| `tests_passed` | 23 |
| `tests_failed` | 1 |

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
| error | `test_result_passed` | test_diamond_shaped_dependency_graph ended with status failed. |

## Delta Summary

Compared `task_scheduler_with_dependencies_v1` → `task_scheduler_with_dependencies_v2`: 0 added, 1 removed, 23 modified.

| Delta ID | Type | TP ID | Before | After |
|---|---|---|---|---|
| `D_1` | removed | `TP_25` | Test large number of tasks and dependencies for performance \| sections=section_1.5 \| type=behavior \| expected=Completes in reasonable time with O((N + E) log N) complexity \| edge=True |  |
| `D_2` | modified | `TP_1` | Verify function signature matches schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) -> list[str] \| sections=section_1.1 \| type=behavior \| expected=Function accepts two parameters (tasks list and dependencies list) and returns a list of strings \| edge=False | Verify function signature matches schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) -> list[str] \| sections=section_2, section_3 \| type=behavior \| expected=Function accepts two parameters (tasks list and dependencies list) and returns a list of strings \| edge=False |
| `D_3` | modified | `TP_10` | Test long linear dependency chain \| sections=section_1.4, section_12, section_13 \| type=behavior \| expected=Returns tasks in correct dependency order \| edge=True | Verify long linear dependency chain maintains correct order \| sections=section_8 \| type=behavior \| expected=Long chain of dependencies is resolved in correct sequential order \| edge=True |
| `D_4` | modified | `TP_11` | Test diamond-shaped dependency graph \| sections=section_1.4, section_14, section_15 \| type=behavior \| expected=Returns ['a', 'b', 'c', 'd'] where 'd' appears after both 'b' and 'c' \| edge=True | Verify multiple independent chains with deterministic ordering \| sections=section_8 \| type=behavior \| expected=Multiple independent dependency chains are ordered deterministically using lexicographic availability \| edge=True |
| `D_5` | modified | `TP_12` | Test multiple independent dependency chains \| sections=section_1.4, section_12, section_13 \| type=behavior \| expected=Returns deterministic ordering respecting all dependencies and lexicographic availability \| edge=True | Verify diamond-shaped dependency graph resolves correctly \| sections=section_8, section_9 \| type=behavior \| expected=schedule_tasks(['a', 'b', 'c', 'd'], [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd')]) returns ['a', 'b', 'c', 'd'] \| edge=True |
| `D_6` | modified | `TP_13` | Test ValueError for duplicate task names \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Raises ValueError when tasks list contains duplicate names \| edge=False | Verify ValueError raised for duplicate task names \| sections=section_7 \| type=behavior \| expected=Raises ValueError when tasks list contains duplicate names \| edge=False |
| `D_7` | modified | `TP_14` | Test ValueError for dependency referring to unknown task \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Raises ValueError when dependency references task not in tasks list \| edge=False | Verify ValueError raised for dependency referencing unknown task \| sections=section_7 \| type=behavior \| expected=Raises ValueError when dependency pair references a task not in tasks list \| edge=False |
| `D_8` | modified | `TP_15` | Test ValueError for circular dependency \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Raises ValueError when circular dependency exists (e.g., A->B->A) \| edge=False | Verify ValueError raised for circular dependency \| sections=section_7 \| type=behavior \| expected=Raises ValueError when circular dependency exists (e.g., A->B->A) \| edge=False |
| `D_9` | modified | `TP_16` | Test TypeError when tasks parameter is not a list \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Raises TypeError for non-list tasks parameter \| edge=False | Verify TypeError raised when tasks is not a list \| sections=section_7 \| type=behavior \| expected=Raises TypeError when tasks parameter is not a list \| edge=False |
| `D_10` | modified | `TP_17` | Test TypeError when dependencies parameter is not a list \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Raises TypeError for non-list dependencies parameter \| edge=False | Verify TypeError raised when dependencies is not a list \| sections=section_7 \| type=behavior \| expected=Raises TypeError when dependencies parameter is not a list \| edge=False |
| `D_11` | modified | `TP_18` | Test TypeError when task name is not a string \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Raises TypeError when tasks list contains non-string elements \| edge=False | Verify TypeError raised when task name is not a string \| sections=section_7 \| type=behavior \| expected=Raises TypeError when any task name in tasks list is not a string \| edge=False |
| `D_12` | modified | `TP_19` | Test TypeError when dependency is not a pair of strings \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Raises TypeError when dependency tuple is malformed or contains non-strings \| edge=False | Verify TypeError raised when dependency is not a pair of strings \| sections=section_8 \| type=behavior \| expected=Raises TypeError when any dependency is not a tuple of two strings \| edge=False |
| `D_13` | modified | `TP_2` | Test basic linear dependency chain execution order \| sections=section_7, section_8, section_9 \| type=behavior \| expected=Returns ['fetch_data', 'clean_data', 'train_model', 'evaluate_model'] for the provided example \| edge=False | Verify linear dependency chain execution order \| sections=section_4, section_5, section_6 \| type=behavior \| expected=Returns ['fetch_data', 'clean_data', 'train_model', 'evaluate_model'] for the provided example \| edge=False |
| `D_14` | modified | `TP_21` | Verify function returns ordering only without executing tasks \| sections=section_1.5 \| type=behavior \| expected=Function returns list of task names without side effects \| edge=False | Verify function returns ordering only without executing tasks \| sections=section_1.5 \| type=behavior \| expected=Function returns a list of task names in order without side effects \| edge=False |
| `D_15` | modified | `TP_22` | Test complex graph with multiple paths and convergence points \| sections=section_1.2, section_1.4 \| type=behavior \| expected=Returns valid topological ordering respecting all dependencies \| edge=True | Verify performance with large task count \| sections=section_1.5 \| type=behavior \| expected=Function completes in reasonable time for large inputs, meeting O((N + E) log N) complexity \| edge=True |
| `D_16` | modified | `TP_23` | Test self-dependency error handling \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Raises ValueError when task has dependency on itself \| edge=True | Verify self-referential dependency raises error \| sections=section_7 \| type=behavior \| expected=Raises ValueError when a task has a dependency on itself \| edge=True |
| `D_17` | modified | `TP_24` | Test empty dependencies list with multiple tasks \| sections=section_1.4, section_12, section_13 \| type=behavior \| expected=Returns tasks in lexicographic order \| edge=False | Verify complex diamond with multiple convergence points \| sections=section_8, section_9 \| type=behavior \| expected=Complex dependency graphs with multiple convergence points resolve correctly \| edge=True |
| `D_18` | modified | `TP_3` | Verify every task in input appears exactly once in output \| sections=section_1.2 \| type=behavior \| expected=All tasks from input list are present in output with no duplicates \| edge=False | Verify every task appears exactly once in output \| sections=section_7 \| type=behavior \| expected=All tasks from input list appear exactly once in the returned ordering \| edge=False |
| `D_19` | modified | `TP_4` | Verify dependency ordering constraint: for each (A, B) pair, A appears before B \| sections=section_1.2 \| type=behavior \| expected=All dependency pairs maintain correct ordering in output \| edge=False | Verify dependency ordering constraint is satisfied \| sections=section_7 \| type=behavior \| expected=For every dependency pair (A, B), task A appears before task B in the output \| edge=False |
| `D_20` | modified | `TP_5` | Test lexicographic ordering when multiple tasks are available \| sections=section_1.2 \| type=behavior \| expected=Returns ['a', 'b', 'c'] for tasks=['b', 'a', 'c'] with empty dependencies \| edge=False | Verify lexicographically largest task selected first when multiple available \| sections=section_7 \| type=behavior \| expected=schedule_tasks(['b', 'a', 'c'], []) returns ['c', 'b', 'a'] \| edge=False |
| `D_21` | modified | `TP_6` | Test deterministic output consistency across multiple calls \| sections=section_1.2 \| type=behavior \| expected=Multiple calls with same input produce identical output \| edge=False | Verify deterministic output across multiple invocations \| sections=section_7 \| type=behavior \| expected=Multiple calls with same inputs produce identical output \| edge=False |
| `D_22` | modified | `TP_7` | Test empty tasks and dependencies boundary condition \| sections=section_1.4, section_12, section_13 \| type=behavior \| expected=Returns empty list [] \| edge=True | Verify empty tasks and dependencies returns empty list \| sections=section_8 \| type=behavior \| expected=schedule_tasks([], []) returns [] \| edge=True |
| `D_23` | modified | `TP_8` | Test single task with no dependencies boundary condition \| sections=section_1.4, section_12, section_13 \| type=behavior \| expected=Returns list containing the single task \| edge=True | Verify single task with no dependencies returns that task \| sections=section_8 \| type=behavior \| expected=schedule_tasks(['task1'], []) returns ['task1'] \| edge=True |
| `D_24` | modified | `TP_9` | Test multiple independent tasks with no dependencies \| sections=section_1.4, section_12, section_13 \| type=behavior \| expected=Returns tasks in lexicographic order \| edge=True | Verify multiple independent tasks return lexicographic order (largest first) \| sections=section_8 \| type=behavior \| expected=schedule_tasks(['x', 'y', 'z'], []) returns ['z', 'y', 'x'] \| edge=True |

## Traceability Matrix

| Source Sections | Test Plan ID | Requirement | Test Functions | Results |
|---|---|---|---|---|
| section_2, section_3 | `TP_1` | Verify function signature matches schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) -> list[str] | `test_function_signature` | passed |
| section_4, section_5, section_6 | `TP_2` | Verify linear dependency chain execution order | `test_linear_dependency_chain_example` | passed |
| section_7 | `TP_3` | Verify every task appears exactly once in output | `test_all_tasks_appear_exactly_once` | passed |
| section_7 | `TP_4` | Verify dependency ordering constraint is satisfied | `test_dependency_ordering_constraint` | passed |
| section_7 | `TP_5` | Verify lexicographically largest task selected first when multiple available | `test_lexicographic_largest_first` | passed |
| section_7 | `TP_6` | Verify deterministic output across multiple invocations | `test_deterministic_output` | passed |
| section_8 | `TP_7` | Verify empty tasks and dependencies returns empty list | `test_empty_tasks_and_dependencies` | passed |
| section_8 | `TP_8` | Verify single task with no dependencies returns that task | `test_single_task_no_dependencies` | passed |
| section_8 | `TP_9` | Verify multiple independent tasks return lexicographic order (largest first) | `test_multiple_independent_tasks_lexicographic` | passed |
| section_8 | `TP_10` | Verify long linear dependency chain maintains correct order | `test_long_linear_dependency_chain` | passed |
| section_8 | `TP_11` | Verify multiple independent chains with deterministic ordering | `test_multiple_independent_chains` | passed |
| section_8, section_9 | `TP_12` | Verify diamond-shaped dependency graph resolves correctly | `test_diamond_shaped_dependency_graph` | failed |
| section_7 | `TP_13` | Verify ValueError raised for duplicate task names | `test_duplicate_task_names_raises_error` | passed |
| section_7 | `TP_14` | Verify ValueError raised for dependency referencing unknown task | `test_unknown_task_in_dependency_raises_error` | passed |
| section_7 | `TP_15` | Verify ValueError raised for circular dependency | `test_circular_dependency_raises_error` | passed |
| section_7 | `TP_16` | Verify TypeError raised when tasks is not a list | `test_tasks_not_list_raises_error` | passed |
| section_7 | `TP_17` | Verify TypeError raised when dependencies is not a list | `test_dependencies_not_list_raises_error` | passed |
| section_7 | `TP_18` | Verify TypeError raised when task name is not a string | `test_task_name_not_string_raises_error` | passed |
| section_8 | `TP_19` | Verify TypeError raised when dependency is not a pair of strings | `test_dependency_not_pair_of_strings_raises_error` | passed |
| section_1.5 | `TP_20` | Verify task names are case-sensitive | `test_case_sensitive_task_names` | passed |
| section_1.5 | `TP_21` | Verify function returns ordering only without executing tasks | `test_function_returns_ordering_only` | passed |
| section_1.5 | `TP_22` | Verify performance with large task count | `test_performance_large_task_count` | passed |
| section_7 | `TP_23` | Verify self-referential dependency raises error | `test_self_referential_dependency_raises_error` | passed |
| section_8, section_9 | `TP_24` | Verify complex diamond with multiple convergence points | `test_complex_diamond_multiple_convergence` | passed |

## Overall Result

Failed validation with 1 error(s) and 3 warning(s).
