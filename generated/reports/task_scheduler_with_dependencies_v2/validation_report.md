# Validation Report: task_scheduler_with_dependencies_v2

## Artifact Summary

| Metric | Value |
|---|---:|
| `version` | task_scheduler_with_dependencies_v2 |
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

Compared `task_scheduler_with_dependencies_v1` → `task_scheduler_with_dependencies_v2`: 0 added, 0 removed, 20 modified.

| Delta ID | Type | TP ID | Before | After |
|---|---|---|---|---|
| `D_1` | modified | `TP_1` | Verify schedule_tasks returns correct ordering for linear dependency chain \| sections=section_7, section_8, section_9 \| type=behavior \| expected=Given tasks [fetch_data, clean_data, train_model, evaluate_model] with dependencies forming a chain, function returns [fetch_data, clean_data, train_model, evaluate_model] \| edge=False | Verify schedule_tasks returns correct ordering for linear dependency chain \| sections=section_4, section_5, section_6 \| type=behavior \| expected=Given tasks [fetch_data, clean_data, train_model, evaluate_model] with linear dependencies, function returns [fetch_data, clean_data, train_model, evaluate_model] \| edge=False |
| `D_2` | modified | `TP_10` | Verify schedule_tasks raises ValueError for duplicate task names \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Given tasks list with duplicate names, function raises ValueError \| edge=True | Verify long dependency chain execution \| sections=section_8 \| type=behavior \| expected=Long linear chain of dependencies is correctly ordered respecting all constraints \| edge=True |
| `D_3` | modified | `TP_11` | Verify schedule_tasks raises ValueError for dependency referencing unknown task \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Given dependency pair where before_task or after_task is not in tasks list, function raises ValueError \| edge=True | Verify ValueError on duplicate task names \| sections=section_7 \| type=error \| expected=Function raises ValueError when tasks list contains duplicate names \| edge=False |
| `D_4` | modified | `TP_12` | Verify schedule_tasks raises ValueError for circular dependency \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Given dependencies that form a cycle (e.g., A→B→C→A), function raises ValueError \| edge=True | Verify ValueError on unknown task in dependency \| sections=section_7 \| type=error \| expected=Function raises ValueError when dependency references a task not in tasks list \| edge=False |
| `D_5` | modified | `TP_13` | Verify schedule_tasks raises ValueError for self-referential dependency \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Given dependency pair (A, A), function raises ValueError \| edge=True | Verify ValueError on circular dependency \| sections=section_7 \| type=error \| expected=Function raises ValueError when circular dependency exists (e.g., A→B→C→A) \| edge=False |
| `D_6` | modified | `TP_14` | Verify schedule_tasks raises TypeError when tasks parameter is not a list \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Given tasks as tuple, dict, string, or other non-list type, function raises TypeError \| edge=True | Verify TypeError when tasks is not a list \| sections=section_7 \| type=error \| expected=Function raises TypeError when tasks parameter is not a list (e.g., tuple, string, dict) \| edge=False |
| `D_7` | modified | `TP_15` | Verify schedule_tasks raises TypeError when dependencies parameter is not a list \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Given dependencies as tuple, dict, string, or other non-list type, function raises TypeError \| edge=True | Verify TypeError when dependencies is not a list \| sections=section_7 \| type=error \| expected=Function raises TypeError when dependencies parameter is not a list \| edge=False |
| `D_8` | modified | `TP_16` | Verify schedule_tasks raises TypeError when task name is not a string \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Given tasks list containing non-string elements (int, None, list), function raises TypeError \| edge=True | Verify TypeError when task name is not a string \| sections=section_7 \| type=error \| expected=Function raises TypeError when any task name is not a string (e.g., int, None, list) \| edge=False |
| `D_9` | modified | `TP_17` | Verify schedule_tasks raises TypeError when dependency is not a pair of strings \| sections=section_1.3, section_10, section_11 \| type=behavior \| expected=Given dependency that is not a 2-tuple of strings (e.g., single string, 3-tuple, tuple with non-strings), function raises TypeError \| edge=True | Verify TypeError when dependency is not a pair of strings \| sections=section_1.3 \| type=error \| expected=Function raises TypeError when dependency tuple is not a pair or contains non-string elements \| edge=False |
| `D_10` | modified | `TP_18` | Verify schedule_tasks is case-sensitive for task names \| sections=section_1.5 \| type=behavior \| expected=Tasks 'Task' and 'task' are treated as distinct tasks \| edge=False | Verify case-sensitive task name handling \| sections=section_1.5 \| type=behavior \| expected=Task names 'Task' and 'task' are treated as distinct tasks \| edge=False |
| `D_11` | modified | `TP_19` | Verify schedule_tasks does not execute tasks or modify external state \| sections=section_1.5 \| type=behavior \| expected=Function returns ordering only without executing tasks, touching files, or modifying global state \| edge=False | Verify function does not execute tasks or modify external state \| sections=section_1.5 \| type=behavior \| expected=Function returns ordering only; no side effects, file operations, or task execution occur \| edge=False |
| `D_12` | modified | `TP_2` | Verify schedule_tasks returns lexicographically sorted order when no dependencies exist \| sections=section_1.2 \| type=behavior \| expected=Given tasks [b, a, c] with empty dependencies, function returns [a, b, c] \| edge=False | Verify lexicographic ordering when no dependencies exist \| sections=section_1.2 \| type=behavior \| expected=Given tasks [b, a, c] with empty dependencies, function returns [c, b, a] (lexicographically largest first) \| edge=False |
| `D_13` | modified | `TP_20` | Verify schedule_tasks handles long dependency chains efficiently \| sections=section_1.4 \| type=behavior \| expected=Given a long linear chain of dependencies, function returns correct ordering respecting all constraints \| edge=False | Verify self-referential dependency is rejected \| sections=section_7 \| type=error \| expected=Function raises ValueError when a task has a dependency on itself (A→A) \| edge=True |
| `D_14` | modified | `TP_3` | Verify schedule_tasks returns empty list for empty inputs \| sections=section_1.4 \| type=behavior \| expected=Given empty tasks list and empty dependencies list, function returns [] \| edge=False | Verify every task appears exactly once in output \| sections=section_1.2 \| type=behavior \| expected=Output list contains all input tasks with no duplicates and length equals input task count \| edge=False |
| `D_15` | modified | `TP_4` | Verify schedule_tasks returns single task when only one task provided \| sections=section_1.4 \| type=behavior \| expected=Given tasks [task1] with no dependencies, function returns [task1] \| edge=False | Verify dependency ordering constraint is satisfied \| sections=section_1.2 \| type=behavior \| expected=For every dependency pair (A, B), A appears at an earlier index than B in the output \| edge=False |
| `D_16` | modified | `TP_5` | Verify schedule_tasks respects all dependency constraints in output \| sections=section_1.2 \| type=behavior \| expected=For every dependency pair (A, B), A appears before B in the returned list \| edge=False | Verify deterministic output on multiple valid orderings \| sections=section_1.2 \| type=behavior \| expected=Multiple calls with same inputs return identical ordering; lexicographic selection ensures determinism \| edge=False |
| `D_17` | modified | `TP_6` | Verify schedule_tasks returns deterministic output with lexicographic tie-breaking \| sections=section_1.2 \| type=behavior \| expected=When multiple tasks are available for execution, the lexicographically smallest is selected first, producing consistent results across multiple calls \| edge=False | Verify diamond-shaped dependency graph handling \| sections=section_8, section_9 \| type=behavior \| expected=Given tasks [a, b, c, d] with diamond dependencies, function returns valid ordering where a precedes b and c, and both b and c precede d \| edge=False |
| `D_18` | modified | `TP_7` | Verify schedule_tasks handles diamond-shaped dependency graph correctly \| sections=section_1.4, section_14, section_15 \| type=behavior \| expected=Given tasks [a, b, c, d] with dependencies [(a, b), (a, c), (b, d), (c, d)], function returns [a, b, c, d] with a first and d last \| edge=False | Verify multiple independent dependency chains \| sections=section_8 \| type=behavior \| expected=Independent chains are ordered deterministically via lexicographic availability; all dependencies within chains are respected \| edge=False |
| `D_19` | modified | `TP_8` | Verify schedule_tasks handles multiple independent dependency chains \| sections=section_1.4 \| type=behavior \| expected=Given multiple independent chains, function returns valid ordering with lexicographic ordering applied to available tasks at each step \| edge=False | Verify empty input returns empty list \| sections=section_8 \| type=behavior \| expected=Given empty tasks list and empty dependencies, function returns [] \| edge=True |
| `D_20` | modified | `TP_9` | Verify schedule_tasks includes every task exactly once in output \| sections=section_1.2 \| type=behavior \| expected=Every task in the input tasks list appears exactly once in the returned execution order \| edge=False | Verify single task with no dependencies \| sections=section_8 \| type=behavior \| expected=Given single task and no dependencies, function returns list containing that task \| edge=True |

## Traceability Matrix

| Source Sections | Test Plan ID | Requirement | Test Functions | Results |
|---|---|---|---|---|
| section_4, section_5, section_6 | `TP_1` | Verify schedule_tasks returns correct ordering for linear dependency chain | `test_linear_dependency_chain` | passed |
| section_1.2 | `TP_2` | Verify lexicographic ordering when no dependencies exist | `test_lexicographic_ordering_no_dependencies` | passed |
| section_1.2 | `TP_3` | Verify every task appears exactly once in output | `test_all_tasks_appear_exactly_once` | passed |
| section_1.2 | `TP_4` | Verify dependency ordering constraint is satisfied | `test_dependency_ordering_constraint` | passed |
| section_1.2 | `TP_5` | Verify deterministic output on multiple valid orderings | `test_deterministic_output` | passed |
| section_8, section_9 | `TP_6` | Verify diamond-shaped dependency graph handling | `test_diamond_dependency_graph` | passed |
| section_8 | `TP_7` | Verify multiple independent dependency chains | `test_multiple_independent_chains` | passed |
| section_8 | `TP_8` | Verify empty input returns empty list | `test_empty_input` | passed |
| section_8 | `TP_9` | Verify single task with no dependencies | `test_single_task_no_dependencies` | passed |
| section_8 | `TP_10` | Verify long dependency chain execution | `test_long_dependency_chain` | passed |
| section_7 | `TP_11` | Verify ValueError on duplicate task names | `test_duplicate_task_names_raises_valueerror` | passed |
| section_7 | `TP_12` | Verify ValueError on unknown task in dependency | `test_unknown_task_in_dependency_raises_valueerror` | passed |
| section_7 | `TP_13` | Verify ValueError on circular dependency | `test_circular_dependency_raises_valueerror` | passed |
| section_7 | `TP_14` | Verify TypeError when tasks is not a list | `test_tasks_not_list_raises_typeerror` | passed |
| section_7 | `TP_15` | Verify TypeError when dependencies is not a list | `test_dependencies_not_list_raises_typeerror` | passed |
| section_7 | `TP_16` | Verify TypeError when task name is not a string | `test_task_name_not_string_raises_typeerror` | passed |
| section_1.3 | `TP_17` | Verify TypeError when dependency is not a pair of strings | `test_dependency_not_pair_of_strings_raises_typeerror` | passed |
| section_1.5 | `TP_18` | Verify case-sensitive task name handling | `test_case_sensitive_task_names` | passed |
| section_1.5 | `TP_19` | Verify function does not execute tasks or modify external state | `test_no_side_effects` | passed |
| section_7 | `TP_20` | Verify self-referential dependency is rejected | `test_self_referential_dependency_raises_valueerror` | passed |

## Overall Result

Passed with 3 warning(s).
