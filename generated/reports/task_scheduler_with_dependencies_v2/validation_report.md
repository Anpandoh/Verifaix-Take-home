# Validation Report: task_scheduler_with_dependencies_v2

## Artifact Summary

| Metric | Value |
|---|---:|
| `version` | task_scheduler_with_dependencies_v2 |
| `description_stored` | True |
| `test_plan_items` | 20 |
| `artifact_count` | 4 |
| `generated_code_records` | 1 |
| `generated_test_records` | 20 |
| `test_results` | 40 |
| `tests_passed` | 40 |
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

Compared `task_scheduler_with_dependencies_v1` → `task_scheduler_with_dependencies_v2`: 0 added, 4 removed, 20 modified.

| Delta ID | Type | TP ID | Before | After |
|---|---|---|---|---|
| `D_1` | removed | `TP_21` | Verify self-referential dependency is rejected \| sections=section_10, section_11 \| type=behavior \| expected=Raises ValueError when a task has a dependency on itself \| edge=True |  |
| `D_2` | removed | `TP_22` | Verify complex multi-level dependency graph \| sections=section_1.2 \| type=behavior \| expected=Complex graphs with multiple levels of dependencies maintain correct ordering \| edge=True |  |
| `D_3` | removed | `TP_23` | Verify empty dependencies list with multiple tasks \| sections=section_1.4 \| type=behavior \| expected=Multiple tasks with no dependencies returns lexicographically sorted list \| edge=True |  |
| `D_4` | removed | `TP_24` | Verify duplicate dependencies are handled correctly \| sections=section_1.2 \| type=behavior \| expected=Duplicate dependency pairs do not affect output correctness \| edge=True |  |
| `D_5` | modified | `TP_1` | Verify function signature matches schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) -> list[str] \| sections=section_1.1 \| type=behavior \| expected=Function accepts two parameters (tasks list and dependencies list) and returns a list of strings \| edge=False | Verify function signature matches API specification \| sections=section_2, section_3 \| type=behavior \| expected=Function schedule_tasks accepts list[str] tasks and list[tuple[str, str]] dependencies, returns list[str] \| edge=False |
| `D_6` | modified | `TP_10` | Verify multiple independent chains are ordered deterministically \| sections=section_1.4 \| type=behavior \| expected=Multiple independent dependency chains are merged with lexicographic ordering of available tasks \| edge=True | Test circular dependency raises ValueError \| sections=section_6 \| type=behavior \| expected=Raises ValueError when circular dependency is detected \| edge=True |
| `D_7` | modified | `TP_11` | Verify long dependency chain execution \| sections=section_1.4 \| type=behavior \| expected=Long linear dependency chains maintain correct ordering \| edge=True | Test tasks parameter is not a list raises TypeError \| sections=section_6 \| type=behavior \| expected=Raises TypeError when tasks is not a list \| edge=True |
| `D_8` | modified | `TP_12` | Verify ValueError on duplicate task names \| sections=section_10, section_11 \| type=behavior \| expected=Raises ValueError when tasks list contains duplicate names \| edge=False | Test dependencies parameter is not a list raises TypeError \| sections=section_6 \| type=behavior \| expected=Raises TypeError when dependencies is not a list \| edge=True |
| `D_9` | modified | `TP_13` | Verify ValueError on dependency referring to unknown task \| sections=section_10, section_11 \| type=behavior \| expected=Raises ValueError when dependency references a task not in tasks list \| edge=False | Test task name is not a string raises TypeError \| sections=section_6 \| type=behavior \| expected=Raises TypeError when any task name is not a string \| edge=True |
| `D_10` | modified | `TP_14` | Verify ValueError on circular dependency detection \| sections=section_10, section_11 \| type=behavior \| expected=Raises ValueError when circular dependency exists \| edge=False | Test dependency pair is not a tuple of strings raises TypeError \| sections=section_6 \| type=behavior \| expected=Raises TypeError when dependency is not a pair of strings \| edge=True |
| `D_11` | modified | `TP_15` | Verify TypeError when tasks parameter is not a list \| sections=section_10, section_11 \| type=behavior \| expected=Raises TypeError when tasks is not a list \| edge=False | Test case sensitivity of task names \| sections=section_2 \| type=behavior \| expected=Task names are treated as case-sensitive; 'Task' and 'task' are different tasks \| edge=False |
| `D_12` | modified | `TP_16` | Verify TypeError when dependencies parameter is not a list \| sections=section_10, section_11 \| type=behavior \| expected=Raises TypeError when dependencies is not a list \| edge=False | Test function does not execute tasks or modify external state \| sections=section_2 \| type=behavior \| expected=Function returns ordering only without executing tasks or touching files \| edge=False |
| `D_13` | modified | `TP_17` | Verify TypeError when task name is not a string \| sections=section_10, section_11 \| type=behavior \| expected=Raises TypeError when any task name is not a string \| edge=False | Test every task appears exactly once in output \| sections=section_6 \| type=behavior \| expected=All tasks from input appear exactly once in returned list \| edge=False |
| `D_14` | modified | `TP_18` | Verify TypeError when dependency is not a pair of strings \| sections=section_10, section_11 \| type=behavior \| expected=Raises TypeError when dependency tuple is malformed or contains non-strings \| edge=False | Test deterministic output on repeated calls \| sections=section_6 \| type=behavior \| expected=Multiple calls with same inputs return identical output \| edge=False |
| `D_15` | modified | `TP_19` | Verify task names are case-sensitive \| sections=section_1.5 \| type=behavior \| expected=Tasks 'Task' and 'task' are treated as different tasks \| edge=False | Test long dependency chain with many tasks \| sections=section_7 \| type=behavior \| expected=Correctly orders long linear chain respecting all dependencies \| edge=True |
| `D_16` | modified | `TP_2` | Verify basic linear dependency chain execution order \| sections=section_7, section_8, section_9 \| type=behavior \| expected=Given tasks [fetch_data, clean_data, train_model, evaluate_model] with linear dependencies, returns [fetch_data, clean_data, train_model, evaluate_model] \| edge=False | Test linear dependency chain execution order \| sections=section_3, section_5 \| type=behavior \| expected=Returns tasks in dependency order: fetch_data -> clean_data -> train_model -> evaluate_model \| edge=False |
| `D_17` | modified | `TP_20` | Verify function does not execute tasks or modify external state \| sections=section_1.5 \| type=behavior \| expected=Function returns ordering only without executing tasks or touching files \| edge=False | Test complex graph with multiple paths and convergence points \| sections=section_7 \| type=behavior \| expected=Returns valid topological sort respecting all dependency constraints \| edge=False |
| `D_18` | modified | `TP_3` | Verify lexicographic ordering when no dependencies exist \| sections=section_1.2 \| type=behavior \| expected=Given tasks [b, a, c] with empty dependencies, returns [a, b, c] \| edge=False | Test lexicographic ordering when no dependencies exist \| sections=section_6 \| type=behavior \| expected=Returns tasks in descending lexicographic order: [c, b, a] \| edge=False |
| `D_19` | modified | `TP_4` | Verify every task appears exactly once in output \| sections=section_1.2 \| type=behavior \| expected=Output list contains all input tasks with no duplicates \| edge=False | Test single task with no dependencies \| sections=section_7 \| type=behavior \| expected=Returns list containing only the single task \| edge=True |
| `D_20` | modified | `TP_5` | Verify dependency ordering constraint is satisfied \| sections=section_1.2 \| type=behavior \| expected=For every dependency pair (A, B), A appears before B in the output \| edge=False | Test empty tasks and dependencies \| sections=section_7 \| type=behavior \| expected=Returns empty list \| edge=True |
| `D_21` | modified | `TP_6` | Verify deterministic output with lexicographic selection \| sections=section_1.2 \| type=behavior \| expected=When multiple tasks are available, lexicographically smallest is selected first \| edge=False | Test diamond-shaped dependency graph \| sections=section_7 \| type=behavior \| expected=Returns [a, b, c, d] where a precedes b and c, and both b and c precede d \| edge=False |
| `D_22` | modified | `TP_7` | Verify diamond-shaped dependency graph handling \| sections=section_14, section_15 \| type=behavior \| expected=Given tasks [a, b, c, d] with diamond dependencies, returns [a, b, c, d] \| edge=False | Test multiple independent dependency chains \| sections=section_7 \| type=behavior \| expected=Returns deterministic ordering respecting all dependencies and using lexicographic ordering for available tasks \| edge=False |
| `D_23` | modified | `TP_8` | Verify empty tasks and dependencies returns empty list \| sections=section_1.4 \| type=behavior \| expected=schedule_tasks([], []) returns [] \| edge=True | Test duplicate task names raises ValueError \| sections=section_6 \| type=behavior \| expected=Raises ValueError with message indicating duplicate task names \| edge=True |
| `D_24` | modified | `TP_9` | Verify single task with no dependencies \| sections=section_1.4 \| type=behavior \| expected=schedule_tasks([task], []) returns [task] \| edge=True | Test dependency references unknown task raises ValueError \| sections=section_6 \| type=behavior \| expected=Raises ValueError when dependency refers to task not in tasks list \| edge=True |

## Traceability Matrix

| Source Sections | Test Plan ID | Requirement | Test Functions | Results |
|---|---|---|---|---|
| section_2, section_3 | `TP_1` | Verify function signature matches API specification | `test_function_signature_api_specification` | passed |
| section_3, section_5 | `TP_2` | Test linear dependency chain execution order | `test_linear_dependency_chain_execution_order` | passed |
| section_6 | `TP_3` | Test lexicographic ordering when no dependencies exist | `test_lexicographic_ordering_no_dependencies` | passed |
| section_7 | `TP_4` | Test single task with no dependencies | `test_single_task_no_dependencies` | passed |
| section_7 | `TP_5` | Test empty tasks and dependencies | `test_empty_tasks_and_dependencies` | passed |
| section_7 | `TP_6` | Test diamond-shaped dependency graph | `test_diamond_shaped_dependency_graph` | passed |
| section_7 | `TP_7` | Test multiple independent dependency chains | `test_multiple_independent_dependency_chains` | passed |
| section_6 | `TP_8` | Test duplicate task names raises ValueError | `test_duplicate_task_names_raises_valueerror` | passed |
| section_6 | `TP_9` | Test dependency references unknown task raises ValueError | `test_dependency_references_unknown_task_raises_valueerror` | passed |
| section_6 | `TP_10` | Test circular dependency raises ValueError | `test_circular_dependency_raises_valueerror` | passed |
| section_6 | `TP_11` | Test tasks parameter is not a list raises TypeError | `test_tasks_parameter_not_list_raises_typeerror` | passed |
| section_6 | `TP_12` | Test dependencies parameter is not a list raises TypeError | `test_dependencies_parameter_not_list_raises_typeerror` | passed |
| section_6 | `TP_13` | Test task name is not a string raises TypeError | `test_task_name_not_string_raises_typeerror` | passed |
| section_6 | `TP_14` | Test dependency pair is not a tuple of strings raises TypeError | `test_dependency_pair_not_tuple_of_strings_raises_typeerror` | passed |
| section_2 | `TP_15` | Test case sensitivity of task names | `test_case_sensitivity_of_task_names` | passed |
| section_2 | `TP_16` | Test function does not execute tasks or modify external state | `test_function_does_not_execute_tasks_or_modify_state` | passed |
| section_6 | `TP_17` | Test every task appears exactly once in output | `test_every_task_appears_exactly_once_in_output` | passed |
| section_6 | `TP_18` | Test deterministic output on repeated calls | `test_deterministic_output_on_repeated_calls` | passed |
| section_7 | `TP_19` | Test long dependency chain with many tasks | `test_long_dependency_chain_with_many_tasks` | passed |
| section_7 | `TP_20` | Test complex graph with multiple paths and convergence points | `test_complex_graph_with_multiple_paths_and_convergence` | passed |

## Overall Result

Passed with 3 warning(s).
