# Test Plan: task_scheduler_with_dependencies_v2

- Description version: `task_scheduler_with_dependencies_v2`
- Test plan items: 20

## Summary

The schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) function computes a valid topological ordering of tasks respecting all dependency constraints. Core success behavior: every task appears exactly once, all dependency pairs (A, B) have A before B, and when multiple tasks are available, lexicographically largest is selected first for deterministic output. Main error cases: ValueError for duplicate tasks, unknown task references, or circular dependencies; TypeError for non-list inputs or non-string task names.

## Test Items

| ID | Type | Edge Case | Source Sections | Description | Expected Behavior |
|---|---|---:|---|---|---|
| `TP_1` | behavior | no | `section_4`, `section_5`, `section_6` | Verify schedule_tasks returns correct ordering for linear dependency chain | Given tasks [fetch_data, clean_data, train_model, evaluate_model] with linear dependencies, function returns [fetch_data, clean_data, train_model, evaluate_model] |
| `TP_2` | behavior | no | `section_1.2` | Verify lexicographic ordering when no dependencies exist | Given tasks [b, a, c] with empty dependencies, function returns [c, b, a] (lexicographically largest first) |
| `TP_3` | behavior | no | `section_1.2` | Verify every task appears exactly once in output | Output list contains all input tasks with no duplicates and length equals input task count |
| `TP_4` | behavior | no | `section_1.2` | Verify dependency ordering constraint is satisfied | For every dependency pair (A, B), A appears at an earlier index than B in the output |
| `TP_5` | behavior | no | `section_1.2` | Verify deterministic output on multiple valid orderings | Multiple calls with same inputs return identical ordering; lexicographic selection ensures determinism |
| `TP_6` | behavior | no | `section_8`, `section_9` | Verify diamond-shaped dependency graph handling | Given tasks [a, b, c, d] with diamond dependencies, function returns valid ordering where a precedes b and c, and both b and c precede d |
| `TP_7` | behavior | no | `section_8` | Verify multiple independent dependency chains | Independent chains are ordered deterministically via lexicographic availability; all dependencies within chains are respected |
| `TP_8` | behavior | yes | `section_8` | Verify empty input returns empty list | Given empty tasks list and empty dependencies, function returns [] |
| `TP_9` | behavior | yes | `section_8` | Verify single task with no dependencies | Given single task and no dependencies, function returns list containing that task |
| `TP_10` | behavior | yes | `section_8` | Verify long dependency chain execution | Long linear chain of dependencies is correctly ordered respecting all constraints |
| `TP_11` | error | no | `section_7` | Verify ValueError on duplicate task names | Function raises ValueError when tasks list contains duplicate names |
| `TP_12` | error | no | `section_7` | Verify ValueError on unknown task in dependency | Function raises ValueError when dependency references a task not in tasks list |
| `TP_13` | error | no | `section_7` | Verify ValueError on circular dependency | Function raises ValueError when circular dependency exists (e.g., A→B→C→A) |
| `TP_14` | error | no | `section_7` | Verify TypeError when tasks is not a list | Function raises TypeError when tasks parameter is not a list (e.g., tuple, string, dict) |
| `TP_15` | error | no | `section_7` | Verify TypeError when dependencies is not a list | Function raises TypeError when dependencies parameter is not a list |
| `TP_16` | error | no | `section_7` | Verify TypeError when task name is not a string | Function raises TypeError when any task name is not a string (e.g., int, None, list) |
| `TP_17` | error | no | `section_1.3` | Verify TypeError when dependency is not a pair of strings | Function raises TypeError when dependency tuple is not a pair or contains non-string elements |
| `TP_18` | behavior | no | `section_1.5` | Verify case-sensitive task name handling | Task names 'Task' and 'task' are treated as distinct tasks |
| `TP_19` | behavior | no | `section_1.5` | Verify function does not execute tasks or modify external state | Function returns ordering only; no side effects, file operations, or task execution occur |
| `TP_20` | error | yes | `section_7` | Verify self-referential dependency is rejected | Function raises ValueError when a task has a dependency on itself (A→A) |
