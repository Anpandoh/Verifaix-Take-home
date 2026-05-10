TEST_PLAN_PROMPT = """\
Create a structured English test plan for the software module description below.

Requirements:
- Return JSON matching the provided schema.
- Use version "{version}" and description_version "{description_version}".
- Create stable item IDs like TP_1, TP_2, ...
- Each item must include source section IDs from the description.
- Cover public API shape, normal behavior, edge cases, errors, assumptions, and constraints.
- Keep item descriptions concise and independently testable.

Description sections:
{sections}
"""


CODE_PROMPT = """\
Generate Python code implementing the module described below.

Requirements:
- Return JSON matching the provided schema.
- Use version "{version}".
- Return one importable Python module as the "code" string.
- Do not include markdown fences.
- Implement only the described public API.
- Raise the described exceptions for invalid inputs.
- Keep the code deterministic and dependency-light.

Description sections:
{sections}

Traceable test plan:
{test_plan}
"""


TESTS_PROMPT = """\
Generate executable pytest tests from the test plan and generated module metadata.

Requirements:
- Return JSON matching the provided schema.
- Use version "{version}".
- Each test "code" string must be valid Python.
- Import the generated module by its module_name.
- Include the relevant test-plan IDs in each test docstring.
- Cover every test-plan item at least once.
- Do not include markdown fences.

Description sections:
{sections}

Traceable test plan:
{test_plan}

Generated module:
{generated_module}
"""
