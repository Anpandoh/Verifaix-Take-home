# Software Generation and Testing Automation

This project implements a take-home pipeline that reads a software module description PDF and generates:

- A traceable structured English test plan
- Python module code implementing the described API
- Executable pytest tests derived from the plan
- SQLite records for descriptions, plans, deltas, generated artifacts, and test results
- A FastAPI/OpenAPI CRUD surface for inspecting stored artifacts

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Set the configured API key environment variable:

```bash
export OPENAI_API_KEY="..."
```

For Anthropic, set `provider = "anthropic"`, use `model_name = "claude-haiku-4-5-20251001"`, and set `api_key_env = "ANTHROPIC_API_KEY"` in `config.toml`.

## Sample Usage

Run the programmatic sample script:

```bash
python sample_use.py
```

The script imports the Python package directly, loads `config.toml` and `.env`, initializes SQLite, runs the v1 and v2 sample PDFs, generates tests/code/reports under `generated/`, compares v2 to v1, validates the outputs, and prints the key artifact paths. `generate()` also supports omitting `version`; in that mode it derives the project name from the PDF header unless `project_name` is supplied, reuses an existing same-hash description, or creates the next `<project>_vN` version and compares it to the prior description for that project.

Start the FastAPI app:

```bash
uvicorn swgen_test_automation.api:app
```

Then inspect OpenAPI docs at `http://127.0.0.1:8000/docs` or the raw spec at `/openapi.json`.

Sample API call:

```bash
curl http://127.0.0.1:8000/health
```

After running `python sample_use.py`, inspect a stored test plan:

```bash
curl http://127.0.0.1:8000/test-plans/sample_v1
```

## E2E LLM Loop Test

The default test suite mocks the LLM boundary. To intentionally stress real LLM structured outputs and generated-code quality, run the opt-in E2E loop:

```bash
RUN_LLM_E2E=1 \
LLM_E2E_LOOPS=3 \
LLM_E2E_PROVIDER=openai \
LLM_E2E_MODEL=gpt-4.1-mini \
python3 -m pytest -m e2e -s
```

Optional knobs:

- `LLM_E2E_PDF`: PDF path to test. Defaults to `/Users/anpandoh/Downloads/Problem_Description_Software_Coding.pdf`.
- `LLM_E2E_API_KEY_ENV`: environment variable name containing the provider API key. Defaults to `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`.
- `LLM_E2E_LOOPS`: number of repeated full pipeline runs.

Each loop runs PDF ingestion, test-plan generation, code generation, pytest generation, generated-test execution, artifact storage, and SQLite assertions. The test aggregates loop failures so repeated runs can show where structured outputs or generated artifacts crack.

## Architecture

The implementation keeps deterministic system behavior separate from LLM generation:

- `ingestion/` extracts PDF text and creates stable section IDs for traceability.
- `generation/` owns prompt templates and Pydantic-backed generation orchestration.
- `llm/` contains the LangChain provider adapter.
- `db/` owns SQLite schema and repository helpers.
- `execute_tests/` runs generated pytest tests and maps results back to test-plan IDs.
- `schemas.py` defines Pydantic contracts for all structured outputs and API responses.
- `api.py` exposes those records through FastAPI and OpenAPI.
- `pipeline.py` orchestrates ingestion, generation, persistence, deltas, and report export.

## Database Content

The SQLite schema stores the assignment artifacts in explicit tables:

- `generated_code`: module name, version, code path, timestamp.
- `generated_tests`: test name, test-plan ID, version, code path, timestamp.
- `description_versions`: ID, project name, version, PDF path, text hash, extracted text, timestamp.
- `test_plan_deltas`: delta ID, old/new version, change type, affected test-plan item, before/after text.

The generic `artifacts` table is retained as file-level metadata for report export and validation.

## Notes

LLM provider, model name, API key environment variable, temperature, database path, and generated-artifact paths are configurable in `config.toml`. The config accepts `provider = "none"` and `use_llm_for_*` toggles to match the assignment surface, but artifact generation currently requires an enabled `openai` or `anthropic` provider and fails early with a clear error otherwise. API keys are never hardcoded or stored in the repository.

LangChain is intentionally contained inside `llm/`; the rest of the application depends only on the local Pydantic contracts and repository/pipeline interfaces. The included unit tests mock the LLM boundary so local validation does not require an API key.
