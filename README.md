# Software Generation and Testing Automation

This project implements a take-home pipeline that reads a software module description PDF and generates:

- A traceable structured English test plan
- Python module code implementing the described API
- Executable pytest tests derived from the plan
- SQLite records for descriptions, plans, deltas, generated artifacts, prompts, and test results
- A FastAPI/OpenAPI CRUD surface for inspecting stored artifacts

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp config.example.toml config.toml
```

Set the configured API key environment variable:

```bash
export OPENAI_API_KEY="..."
```

For Anthropic, set `provider = "anthropic"`, update `model_name`, and set `api_key_env = "ANTHROPIC_API_KEY"` in `config.toml`.

## Commands

Initialize the SQLite database:

```bash
swgen init-db
```

Generate a plan, module, and tests from the sample PDF:

```bash
swgen generate \
  --pdf "/Users/anpandoh/Downloads/Problem_Description_Software_Coding.pdf" \
  --version v1
```

Run generated pytest tests and persist results:

```bash
swgen run-tests --version v1
```

Generate an updated version and compare test-plan deltas:

```bash
swgen generate --pdf path/to/updated.pdf --version v2 --compare-to v1
swgen show-deltas --version v2
```

Export a human-readable report:

```bash
swgen export-report --version v1
```

Start the FastAPI app:

```bash
swgen serve
```

Then inspect OpenAPI docs at `http://127.0.0.1:8000/docs` or the raw spec at `/openapi.json`.

## E2E LLM Loop Test

The default test suite mocks the LLM boundary. To intentionally stress real LLM structured outputs and generated-code quality, run the opt-in E2E loop:

```bash
RUN_LLM_E2E=1 \
LLM_E2E_LOOPS=3 \
LLM_E2E_PROVIDER=openai \
LLM_E2E_MODEL=gpt-4.1-mini \
python -m pytest -m e2e -s
```

Optional knobs:

- `LLM_E2E_PDF`: PDF path to test. Defaults to `/Users/anpandoh/Downloads/Problem_Description_Software_Coding.pdf`.
- `LLM_E2E_API_KEY_ENV`: environment variable name containing the provider API key. Defaults to `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`.
- `LLM_E2E_LOOPS`: number of repeated full pipeline runs.

Each loop runs PDF ingestion, test-plan generation, code generation, pytest generation, generated-test execution, prompt storage, artifact storage, and SQLite assertions. The test aggregates loop failures so repeated runs can show where structured outputs or generated artifacts crack.

## Architecture

The implementation keeps deterministic system behavior separate from LLM generation:

- `pdf_reader.py` extracts and normalizes PDF text.
- `section_parser.py` creates stable section IDs for traceability.
- `schemas.py` defines Pydantic contracts for all structured outputs and API responses.
- `llm_client.py` uses LangChain provider adapters for OpenAI or Anthropic structured outputs and validates responses through Pydantic.
- `generators.py` renders prompts for test plans, module code, and pytest suites.
- `database.py` owns SQLite initialization and CRUD helpers.
- `api.py` exposes those records through FastAPI and OpenAPI.
- `pipeline.py` orchestrates ingestion, generation, persistence, deltas, and report export.
- `runner.py` executes generated pytest tests and maps results back to test-plan IDs.

## Notes

LLM provider, model name, API key environment variable, temperature, database path, and generated-artifact paths are configurable in `config.toml`. API keys are never hardcoded or stored in the repository.

LangChain is intentionally contained inside `llm_client.py`; the rest of the application depends only on the local Pydantic contracts and repository/pipeline interfaces. The included unit tests mock the LLM boundary so local validation does not require an API key.
