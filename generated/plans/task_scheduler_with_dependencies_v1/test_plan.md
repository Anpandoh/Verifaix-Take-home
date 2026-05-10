# Test Plan: task_scheduler_with_dependencies_v1

- Description version: `task_scheduler_with_dependencies_v1`
- Test plan items: 20

## Summary

The schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) function computes a valid topological ordering of tasks respecting all dependency constraints. It returns a list[str] containing each task exactly once, ordered such that for every dependency pair (A, B), A appears before B, with ties broken lexicographically. The function must reject invalid inputs (non-list types, non-string task names, unknown task references, circular dependencies) with appropriate TypeError or ValueError exceptions, and handle boundary cases including empty inputs, single tasks, and complex dependency graphs like diamond patterns.

## Test Items

| ID | Type | Edge Case | Source Sections | Description | Expected Behavior |
|---|---|---:|---|---|---|
| `TP_1` | behavior | no | `section_7`, `section_8`, `section_9` | Verify schedule_tasks returns correct ordering for linear dependency chain | Given tasks [fetch_data, clean_data, train_model, evaluate_model] with dependencies forming a chain, function returns [fetch_data, clean_data, train_model, evaluate_model] |
| `TP_2` | behavior | no | `section_1.2` | Verify schedule_tasks returns lexicographically sorted order when no dependencies exist | Given tasks [b, a, c] with empty dependencies, function returns [a, b, c] |
| `TP_3` | behavior | no | `section_1.4` | Verify schedule_tasks returns empty list for empty inputs | Given empty tasks list and empty dependencies list, function returns [] |
| `TP_4` | behavior | no | `section_1.4` | Verify schedule_tasks returns single task when only one task provided | Given tasks [task1] with no dependencies, function returns [task1] |
| `TP_5` | behavior | no | `section_1.2` | Verify schedule_tasks respects all dependency constraints in output | For every dependency pair (A, B), A appears before B in the returned list |
| `TP_6` | behavior | no | `section_1.2` | Verify schedule_tasks returns deterministic output with lexicographic tie-breaking | When multiple tasks are available for execution, the lexicographically smallest is selected first, producing consistent results across multiple calls |
| `TP_7` | behavior | no | `section_1.4`, `section_14`, `section_15` | Verify schedule_tasks handles diamond-shaped dependency graph correctly | Given tasks [a, b, c, d] with dependencies [(a, b), (a, c), (b, d), (c, d)], function returns [a, b, c, d] with a first and d last |
| `TP_8` | behavior | no | `section_1.4` | Verify schedule_tasks handles multiple independent dependency chains | Given multiple independent chains, function returns valid ordering with lexicographic ordering applied to available tasks at each step |
| `TP_9` | behavior | no | `section_1.2` | Verify schedule_tasks includes every task exactly once in output | Every task in the input tasks list appears exactly once in the returned execution order |
| `TP_10` | behavior | yes | `section_1.3`, `section_10`, `section_11` | Verify schedule_tasks raises ValueError for duplicate task names | Given tasks list with duplicate names, function raises ValueError |
| `TP_11` | behavior | yes | `section_1.3`, `section_10`, `section_11` | Verify schedule_tasks raises ValueError for dependency referencing unknown task | Given dependency pair where before_task or after_task is not in tasks list, function raises ValueError |
| `TP_12` | behavior | yes | `section_1.3`, `section_10`, `section_11` | Verify schedule_tasks raises ValueError for circular dependency | Given dependencies that form a cycle (e.g., A→B→C→A), function raises ValueError |
| `TP_13` | behavior | yes | `section_1.3`, `section_10`, `section_11` | Verify schedule_tasks raises ValueError for self-referential dependency | Given dependency pair (A, A), function raises ValueError |
| `TP_14` | behavior | yes | `section_1.3`, `section_10`, `section_11` | Verify schedule_tasks raises TypeError when tasks parameter is not a list | Given tasks as tuple, dict, string, or other non-list type, function raises TypeError |
| `TP_15` | behavior | yes | `section_1.3`, `section_10`, `section_11` | Verify schedule_tasks raises TypeError when dependencies parameter is not a list | Given dependencies as tuple, dict, string, or other non-list type, function raises TypeError |
| `TP_16` | behavior | yes | `section_1.3`, `section_10`, `section_11` | Verify schedule_tasks raises TypeError when task name is not a string | Given tasks list containing non-string elements (int, None, list), function raises TypeError |
| `TP_17` | behavior | yes | `section_1.3`, `section_10`, `section_11` | Verify schedule_tasks raises TypeError when dependency is not a pair of strings | Given dependency that is not a 2-tuple of strings (e.g., single string, 3-tuple, tuple with non-strings), function raises TypeError |
| `TP_18` | behavior | no | `section_1.5` | Verify schedule_tasks is case-sensitive for task names | Tasks 'Task' and 'task' are treated as distinct tasks |
| `TP_19` | behavior | no | `section_1.5` | Verify schedule_tasks does not execute tasks or modify external state | Function returns ordering only without executing tasks, touching files, or modifying global state |
| `TP_20` | behavior | no | `section_1.4` | Verify schedule_tasks handles long dependency chains efficiently | Given a long linear chain of dependencies, function returns correct ordering respecting all constraints |
