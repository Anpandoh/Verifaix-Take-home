# Coding Agents And LLMs Used

## Development Agent

Cursor coding agent was used to design and implement the project scaffold, Python package, SQLite persistence layer, FastAPI API, CLI, tests, and documentation.

## Runtime LLMs

The application supports configurable third-party LLM providers:

- OpenAI via `provider = "openai"`
- Anthropic via `provider = "anthropic"`

Provider calls are routed through LangChain chat model adapters with `.with_structured_output(...)`, while the application keeps its own Pydantic schemas, pipeline, persistence, and traceability logic.

The provider, model name, API key environment variable, and temperature are configured in `config.toml`.

`provider = "none"` is accepted by configuration parsing to match the assignment's config surface,
but this implementation requires an enabled third-party provider for test-plan, code, and test
generation. If `provider = "none"` or a `use_llm_for_*` generation toggle is disabled, the pipeline
fails before making any generation attempt and explains which setting must be changed.

The implementation intentionally does not depend on vLLM or local model serving. The assignment focuses on generation orchestration, traceability, persistence, and test execution rather than model hosting.
