# Prompts Used

The runtime prompts are defined in `src/swgen_test_automation/generators.py` and persisted to the `prompts` SQLite table for each generation run.

## Test Plan Prompt

The test-plan prompt asks the model to return Pydantic-validated JSON containing concise, independently testable items with stable IDs, source sections, expected behavior, test type, and edge-case flags.

## Code Prompt

The code prompt asks the model to return a single importable Python module inside a validated `GeneratedModule` envelope. The prompt includes the original description sections and traceable test plan.

## Test Prompt

The pytest prompt asks the model to return executable pytest functions inside a validated `GeneratedTestSuite` envelope. Each generated test must include related test-plan IDs in its docstring.

## Prompt Storage

Every call records:

- Version
- Prompt type
- Rendered prompt text
- Provider
- Model name
- Timestamp
