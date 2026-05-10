# Validation Report: sample_v2

## Artifact Summary

| Metric | Value |
|---|---:|
| `version` | sample_v2 |
| `description_stored` | True |
| `test_plan_items` | 22 |
| `artifact_count` | 4 |
| `generated_code_records` | 1 |
| `generated_test_records` | 22 |
| `test_results` | 70 |
| `tests_passed` | 69 |
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
| error | `result_references_known_tp` | Result references unknown TP_23. |
| error | `result_references_known_tp` | Result references unknown TP_24. |
| error | `test_result_passed` | test_case_sensitive_task_names ended with status failed. |

## Delta Summary

Compared `sample_v1` → `sample_v2`: 0 added, 3 removed, 22 modified.

| Delta ID | Type | TP ID | Before | After |
|---|---|---|---|---|
| `D_1` | removed | `TP_23` | Verify complex multi-level dependency graph \| sections=section_1.2 \| type=behavior \| expected=Correctly orders tasks with multiple levels of transitive dependencies \| edge=True |  |
| `D_2` | removed | `TP_24` | Verify empty dependencies list with multiple tasks \| sections=section_1.4, section_12, section_13 \| type=behavior \| expected=Returns tasks in lexicographic order when no dependencies exist \| edge=True |  |
| `D_3` | removed | `TP_25` | Verify performance with large task count \| sections=section_1.5 \| type=behavior \| expected=Completes within O((N + E) log N) time complexity for large inputs \| edge=True |  |
| `D_4` | modified | `TP_1` | Verify function signature matches schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) -> list[str] \| sections=section_2, section_1.1 \| type=behavior \| expected=Function accepts two parameters (tasks list and dependencies list) and returns a list of strings \| edge=False | Verify function signature accepts tasks list and dependencies list, returns list of strings \| sections=section_2, section_3 \| type=behavior \| expected=schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) -> list[str] is callable and returns a list \| edge=False |
| `D_5` | modified | `TP_10` | Verify long linear dependency chain maintains order \| sections=section_1.4, section_12, section_13 \| type=behavior \| expected=Long chain of dependencies is ordered correctly from first to last \| edge=True | Verify multiple independent dependency chains are ordered deterministically \| sections=section_7 \| type=behavior \| expected=Multiple independent chains respect internal ordering and use lexicographic selection for cross-chain ordering \| edge=True |
| `D_6` | modified | `TP_11` | Verify diamond-shaped dependency graph resolves correctly \| sections=section_1.4, section_14, section_15 \| type=behavior \| expected=Returns ['a', 'b', 'c', 'd'] for diamond graph with a as root and d as sink \| edge=True | Verify diamond-shaped dependency graph resolves correctly \| sections=section_7 \| type=behavior \| expected=schedule_tasks(['a', 'b', 'c', 'd'], [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'd')]) returns ['a', 'b', 'c', 'd'] \| edge=True |
| `D_7` | modified | `TP_12` | Verify multiple independent chains with lexicographic tie-breaking \| sections=section_1.4, section_12, section_13 \| type=behavior \| expected=Independent chains are ordered deterministically using lexicographic availability \| edge=True | Verify ValueError raised for duplicate task names \| sections=section_6 \| type=behavior \| expected=schedule_tasks(['task1', 'task1'], []) raises ValueError \| edge=False |
| `D_8` | modified | `TP_13` | Verify ValueError raised for duplicate task names \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Raises ValueError when tasks list contains duplicate names \| edge=False | Verify ValueError raised when dependency references unknown task \| sections=section_6 \| type=behavior \| expected=schedule_tasks(['a', 'b'], [('a', 'unknown')]) raises ValueError \| edge=False |
| `D_9` | modified | `TP_14` | Verify ValueError raised when dependency references unknown task \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Raises ValueError when dependency pair contains task not in tasks list \| edge=False | Verify ValueError raised for circular dependency \| sections=section_6 \| type=behavior \| expected=schedule_tasks(['a', 'b'], [('a', 'b'), ('b', 'a')]) raises ValueError \| edge=False |
| `D_10` | modified | `TP_15` | Verify ValueError raised for circular dependency \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Raises ValueError when circular dependency exists (e.g., A->B->A) \| edge=False | Verify TypeError raised when tasks parameter is not a list \| sections=section_6 \| type=behavior \| expected=schedule_tasks('not_a_list', []) raises TypeError \| edge=False |
| `D_11` | modified | `TP_16` | Verify TypeError raised when tasks parameter is not a list \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Raises TypeError when tasks is tuple, string, dict, or non-list type \| edge=False | Verify TypeError raised when dependencies parameter is not a list \| sections=section_6 \| type=behavior \| expected=schedule_tasks(['a'], 'not_a_list') raises TypeError \| edge=False |
| `D_12` | modified | `TP_17` | Verify TypeError raised when dependencies parameter is not a list \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Raises TypeError when dependencies is tuple, string, dict, or non-list type \| edge=False | Verify TypeError raised when task name is not a string \| sections=section_6 \| type=behavior \| expected=schedule_tasks([1, 2, 3], []) raises TypeError \| edge=False |
| `D_13` | modified | `TP_18` | Verify TypeError raised when task name is not a string \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Raises TypeError when tasks list contains non-string elements (int, None, etc.) \| edge=False | Verify TypeError raised when dependency is not a pair of strings \| sections=section_6 \| type=behavior \| expected=schedule_tasks(['a', 'b'], [('a',)]) raises TypeError \| edge=False |
| `D_14` | modified | `TP_19` | Verify TypeError raised when dependency is not a pair of strings \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Raises TypeError when dependency tuple contains non-string elements or is not a 2-tuple \| edge=False | Verify task names are case-sensitive \| sections=section_2 \| type=behavior \| expected=schedule_tasks(['Task', 'task'], []) treats them as distinct tasks \| edge=False |
| `D_15` | modified | `TP_2` | Verify basic linear dependency chain is ordered correctly \| sections=section_7, section_8, section_9 \| type=behavior \| expected=Returns ['fetch_data', 'clean_data', 'train_model', 'evaluate_model'] for the provided example \| edge=False | Verify all tasks from input appear exactly once in output \| sections=section_2, section_3 \| type=behavior \| expected=Output list contains all input tasks with no duplicates \| edge=False |
| `D_16` | modified | `TP_20` | Verify task names are case-sensitive \| sections=section_1.5 \| type=behavior \| expected=Tasks 'Task' and 'task' are treated as distinct tasks \| edge=False | Verify function returns ordering only without executing tasks \| sections=section_2 \| type=behavior \| expected=Function returns list of task names without side effects or file operations \| edge=False |
| `D_17` | modified | `TP_21` | Verify function returns ordering only without executing tasks \| sections=section_1.5 \| type=behavior \| expected=Function returns list of task names without side effects or file operations \| edge=False | Verify self-referential dependency raises ValueError \| sections=section_6 \| type=behavior \| expected=schedule_tasks(['a'], [('a', 'a')]) raises ValueError for circular dependency \| edge=True |
| `D_18` | modified | `TP_22` | Verify self-dependency is detected as circular \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Raises ValueError when task has dependency on itself (A, A) \| edge=True | Verify complex graph with multiple paths to same node \| sections=section_7 \| type=behavior \| expected=Tasks with multiple dependency paths are scheduled after all prerequisites \| edge=True |
| `D_19` | modified | `TP_3` | Verify every task in input appears exactly once in output \| sections=section_1.2 \| type=behavior \| expected=All tasks from input list appear in output list with no duplicates \| edge=False | Verify dependency ordering is respected for simple linear chain \| sections=section_2, section_3, section_5 \| type=behavior \| expected=For dependencies (A, B), A appears before B in output. Example: fetch_data before clean_data before train_model before evaluate_model \| edge=False |
| `D_20` | modified | `TP_4` | Verify dependency ordering constraint: for each (A, B) pair, A appears before B \| sections=section_1.2 \| type=behavior \| expected=For every dependency (A, B), index of A in output is less than index of B \| edge=False | Verify lexicographically largest task is selected first when multiple tasks are available \| sections=section_2, section_6 \| type=behavior \| expected=schedule_tasks(['b', 'a', 'c'], []) returns ['c', 'b', 'a'] \| edge=False |
| `D_21` | modified | `TP_5` | Verify lexicographic ordering when multiple tasks are available \| sections=section_1.2 \| type=behavior \| expected=Returns ['a', 'b', 'c'] for schedule_tasks(['b', 'a', 'c'], []) \| edge=False | Verify deterministic output across multiple invocations with same input \| sections=section_2, section_6 \| type=behavior \| expected=Multiple calls with identical inputs produce identical outputs \| edge=False |
| `D_22` | modified | `TP_6` | Verify deterministic output across multiple invocations \| sections=section_1.2 \| type=behavior \| expected=Same input produces identical output on repeated calls \| edge=False | Verify empty tasks and dependencies returns empty list \| sections=section_7 \| type=behavior \| expected=schedule_tasks([], []) returns [] \| edge=True |
| `D_23` | modified | `TP_7` | Verify empty input returns empty output \| sections=section_1.4, section_12, section_13 \| type=behavior \| expected=schedule_tasks([], []) returns [] \| edge=True | Verify single task with no dependencies returns that task \| sections=section_7 \| type=behavior \| expected=schedule_tasks(['task1'], []) returns ['task1'] \| edge=True |
| `D_24` | modified | `TP_8` | Verify single task with no dependencies returns that task \| sections=section_1.4, section_12, section_13 \| type=behavior \| expected=schedule_tasks(['task1'], []) returns ['task1'] \| edge=True | Verify multiple independent tasks return in lexicographic order (largest first) \| sections=section_7 \| type=behavior \| expected=schedule_tasks(['x', 'y', 'z'], []) returns ['z', 'y', 'x'] \| edge=True |
| `D_25` | modified | `TP_9` | Verify multiple independent tasks return lexicographic order \| sections=section_1.4, section_12, section_13 \| type=behavior \| expected=schedule_tasks(['z', 'a', 'm'], []) returns ['a', 'm', 'z'] \| edge=True | Verify long linear dependency chain maintains correct order \| sections=section_7 \| type=behavior \| expected=Long chain of dependencies (A->B->C->D->E) returns tasks in dependency order \| edge=True |

## Traceability Matrix

| Source Sections | Test Plan ID | Requirement | Test Functions | Results |
|---|---|---|---|---|
| section_2, section_3 | `TP_1` | Verify function signature accepts tasks list and dependencies list, returns list of strings | `test_function_signature_and_return_type` | passed |
| section_2, section_3 | `TP_2` | Verify all tasks from input appear exactly once in output | `test_all_tasks_appear_exactly_once` | passed |
| section_2, section_3, section_5 | `TP_3` | Verify dependency ordering is respected for simple linear chain | `test_simple_linear_dependency_chain` | passed |
| section_2, section_6 | `TP_4` | Verify lexicographically largest task is selected first when multiple tasks are available | `test_lexicographic_ordering_no_dependencies` | passed |
| section_2, section_6 | `TP_5` | Verify deterministic output across multiple invocations with same input | `test_deterministic_output` | passed |
| section_7 | `TP_6` | Verify empty tasks and dependencies returns empty list | `test_empty_tasks_and_dependencies` | passed |
| section_7 | `TP_7` | Verify single task with no dependencies returns that task | `test_single_task_no_dependencies` | passed |
| section_7 | `TP_8` | Verify multiple independent tasks return in lexicographic order (largest first) | `test_multiple_independent_tasks_lexicographic_order` | passed |
| section_7 | `TP_9` | Verify long linear dependency chain maintains correct order | `test_long_linear_dependency_chain` | passed |
| section_7 | `TP_10` | Verify multiple independent dependency chains are ordered deterministically | `test_multiple_independent_chains` | passed |
| section_7 | `TP_11` | Verify diamond-shaped dependency graph resolves correctly | `test_diamond_shaped_dependency_graph` | passed |
| section_6 | `TP_12` | Verify ValueError raised for duplicate task names | `test_duplicate_task_names_raises_valueerror` | passed |
| section_6 | `TP_13` | Verify ValueError raised when dependency references unknown task | `test_unknown_task_in_dependency_raises_valueerror` | passed |
| section_6 | `TP_14` | Verify ValueError raised for circular dependency | `test_circular_dependency_raises_valueerror` | passed |
| section_6 | `TP_15` | Verify TypeError raised when tasks parameter is not a list | `test_tasks_not_list_raises_typeerror` | passed |
| section_6 | `TP_16` | Verify TypeError raised when dependencies parameter is not a list | `test_dependencies_not_list_raises_typeerror` | passed |
| section_6 | `TP_17` | Verify TypeError raised when task name is not a string | `test_task_name_not_string_raises_typeerror` | passed |
| section_6 | `TP_18` | Verify TypeError raised when dependency is not a pair of strings | `test_dependency_not_pair_of_strings_raises_typeerror` | passed |
| section_2 | `TP_19` | Verify task names are case-sensitive | `test_case_sensitive_task_names` | failed, passed |
| section_2 | `TP_20` | Verify function returns ordering only without executing tasks | `test_function_returns_ordering_only` | passed |
| section_6 | `TP_21` | Verify self-referential dependency raises ValueError | `test_self_referential_dependency_raises_valueerror` | passed |
| section_7 | `TP_22` | Verify complex graph with multiple paths to same node | `test_complex_graph_multiple_paths` | passed |

## Overall Result

Failed validation with 3 error(s) and 3 warning(s).
