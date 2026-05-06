from __future__ import annotations

import os
from pathlib import Path

import pytest

from swgen_test_automation import pipeline
from swgen_test_automation.database import Repository


DEFAULT_SAMPLE_PDF = "/Users/anpandoh/Downloads/Problem_Description_Software_Coding.pdf"


@pytest.mark.e2e
def test_real_llm_pipeline_loop_surfaces_structured_output_and_generation_cracks(
    tmp_path: Path,
) -> None:
    if os.getenv("RUN_LLM_E2E") != "1":
        pytest.skip("Set RUN_LLM_E2E=1 to run repeated real-LLM pipeline checks.")

    loops = int(os.getenv("LLM_E2E_LOOPS", "3"))
    provider = os.getenv("LLM_E2E_PROVIDER", "openai")
    model_name = os.getenv("LLM_E2E_MODEL", "gpt-4.1-mini")
    api_key_env = os.getenv("LLM_E2E_API_KEY_ENV") or _default_api_key_env(provider)
    pdf_path = Path(os.getenv("LLM_E2E_PDF", DEFAULT_SAMPLE_PDF))

    if loops < 1:
        pytest.fail("LLM_E2E_LOOPS must be at least 1.")
    if not pdf_path.exists():
        pytest.fail(f"E2E PDF does not exist: {pdf_path}")
    if not os.getenv(api_key_env):
        pytest.fail(f"Set {api_key_env} before running RUN_LLM_E2E=1.")

    config_path = _write_e2e_config(tmp_path, provider, model_name, api_key_env)
    failures: list[str] = []

    for index in range(1, loops + 1):
        version = f"e2e_loop_{index}"
        try:
            plan = pipeline.generate(pdf_path, version, config_path=config_path)
            if not plan.items:
                failures.append(f"{version}: generated test plan had no items")
                continue

            results = pipeline.run_tests(version, config_path=config_path)
            failed_results = [result for result in results if result.status.value != "passed"]
            if failed_results:
                failures.append(
                    f"{version}: generated tests failed\n"
                    + "\n".join(
                        f"- {result.test_name}: {result.failure_message}"
                        for result in failed_results
                    )
                )

            repo = Repository(tmp_path / "e2e.sqlite")
            _assert_required_records(repo, version)
        except Exception as exc:  # noqa: BLE001 - E2E should aggregate all loop failures.
            failures.append(f"{version}: {type(exc).__name__}: {exc}")

    if failures:
        pytest.fail(
            "Real-LLM E2E loop found generation or structured-output cracks:\n\n"
            + "\n\n".join(failures)
        )


def _write_e2e_config(
    tmp_path: Path,
    provider: str,
    model_name: str,
    api_key_env: str,
) -> Path:
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        f"""
[app]
database_path = "{tmp_path / "e2e.sqlite"}"
generated_dir = "{tmp_path / "generated"}"
reports_dir = "{tmp_path / "reports"}"

[llm]
provider = "{provider}"
model_name = "{model_name}"
api_key_env = "{api_key_env}"
temperature = 0.1
use_llm_for_testplan = true
use_llm_for_code = true
use_llm_for_tests = true
""",
        encoding="utf-8",
    )
    return config_path


def _assert_required_records(repo: Repository, version: str) -> None:
    plan = repo.get_test_plan(version)
    assert plan is not None, f"{version}: missing stored test plan"
    assert repo.get_artifacts(version, "test_plan"), f"{version}: missing test-plan artifact"
    assert repo.get_artifacts(version, "generated_code"), f"{version}: missing code artifact"
    assert repo.get_artifacts(version, "generated_tests"), f"{version}: missing tests artifact"
    assert repo.get_execution_results(version), f"{version}: missing execution results"
    assert len(repo.get_prompts(version)) == 3, f"{version}: expected 3 stored prompts"


def _default_api_key_env(provider: str) -> str:
    if provider == "anthropic":
        return "ANTHROPIC_API_KEY"
    return "OPENAI_API_KEY"
