from pathlib import Path

import pytest

from swgen_test_automation import schemas
from swgen_test_automation import pipeline
from swgen_test_automation.ingestion import StyledTextLine


SAMPLE_TEXT = """Problem Description: Task Scheduler with Dependencies
1. Overview
A Python module that computes a valid execution order for tasks with dependencies.
1.1 API
schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) -> list[str]
1.2 Ordering Rules
Every task appears exactly once.
"""

SAMPLE_TEXT_V2 = SAMPLE_TEXT + "1.3 Validation\nInvalid inputs raise ValueError.\n"


class FakeLLM:
    def generate_model(self, prompt: str, model_type: type):
        version = _prompt_value(prompt, "version") or "v1"
        description_version = _prompt_value(prompt, "description_version") or version
        expected_behavior = (
            "callable validates invalid inputs"
            if "Invalid inputs raise ValueError" in prompt
            else "callable is present"
        )
        if model_type is schemas.TestPlan:
            return schemas.TestPlan(
                version=version,
                description_version=description_version,
                summary=(
                    "Tests schedule_tasks(tasks, dependencies) for topological ordering, "
                    "deterministic tie-breaking, and invalid dependency inputs."
                ),
                items=[
                    schemas.TestPlanItem(
                        id="TP_1",
                        description="Module exposes schedule_tasks",
                        source_sections=["1.1"],
                        expected_behavior=expected_behavior,
                    )
                ],
            )
        if model_type is schemas.GeneratedModule:
            return schemas.GeneratedModule(
                version=version,
                module_name="task_scheduler",
                public_api=["schedule_tasks"],
                source_sections=["1.1"],
                test_plan_item_ids=["TP_1"],
                code=(
                    "def schedule_tasks(tasks, dependencies):\n"
                    "    if not tasks:\n"
                    "        return []\n"
                    "    return sorted(tasks)\n"
                ),
            )
        if model_type is schemas.GeneratedTestSuite:
            return schemas.GeneratedTestSuite(
                version=version,
                tests=[
                    schemas.GeneratedTest(
                        name="test_tp_1_callable",
                        test_plan_item_ids=["TP_1"],
                        code=(
                            "from task_scheduler import schedule_tasks\n\n"
                            "def test_tp_1_callable():\n"
                            "    \"\"\"TP_1: Module exposes schedule_tasks.\"\"\"\n"
                            "    assert schedule_tasks([], []) == []\n"
                        ),
                    )
                ],
            )
        raise AssertionError(model_type)


def _prompt_value(prompt: str, field_name: str) -> str | None:
    marker = f'{field_name} "'
    if marker not in prompt:
        return None
    return prompt.split(marker, 1)[1].split('"', 1)[0]


def test_pipeline_generates_and_persists_artifacts_with_mocked_llm(
    tmp_path: Path,
    monkeypatch,
) -> None:
    config = tmp_path / "config.toml"
    config.write_text(
        f"""
[app]
database_path = "{tmp_path / "db.sqlite"}"
generated_dir = "{tmp_path / "generated"}"
reports_dir = "{tmp_path / "generated" / "reports"}"

[llm]
provider = "openai"
model_name = "fake-model"
api_key_env = "FAKE_API_KEY"
temperature = 0.1
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        pipeline,
        "extract_pdf_lines",
        lambda _path: [StyledTextLine(line) for line in SAMPLE_TEXT.splitlines()],
    )
    monkeypatch.setattr(pipeline, "LLMClient", lambda _settings: FakeLLM())

    plan = pipeline.generate(tmp_path / "input.pdf", "v1", config_path=config)
    results = pipeline.run_tests("v1", config_path=config)
    report_path = pipeline.export_report("v1", config_path=config)

    assert plan.items[0].id == "TP_1"
    assert results[0].status.value == "passed"
    assert (tmp_path / "generated" / "code" / "v1" / "task_scheduler.py").exists()
    repo = pipeline.Repository(tmp_path / "db.sqlite")
    generated_code = repo.get_generated_code("v1")
    generated_tests = repo.get_generated_tests("v1")
    assert generated_code[0].module_name == "task_scheduler"
    assert generated_code[0].version == "v1"
    assert generated_code[0].code_path.name == "task_scheduler.py"
    assert generated_tests[0].test_name == "test_tp_1_callable"
    assert generated_tests[0].test_plan_item_id == "TP_1"
    assert generated_tests[0].code_path.name == "test_generated.py"
    plan_markdown = tmp_path / "generated" / "plans" / "v1" / "test_plan.md"
    assert plan_markdown.exists()
    assert "schedule_tasks(tasks, dependencies)" in plan_markdown.read_text(encoding="utf-8")
    assert (report_path / "test_plan.json").exists()
    assert (report_path / "test_plan.md").exists()
    assert (report_path / "generated_code.json").exists()
    assert (report_path / "generated_tests.json").exists()
    assert not (report_path / "prompts.json").exists()


def test_pipeline_auto_versions_by_project_and_compares_previous_description(
    tmp_path: Path,
    monkeypatch,
) -> None:
    config = tmp_path / "config.toml"
    config.write_text(
        f"""
[app]
database_path = "{tmp_path / "db.sqlite"}"
generated_dir = "{tmp_path / "generated"}"
reports_dir = "{tmp_path / "generated" / "reports"}"

[llm]
provider = "openai"
model_name = "fake-model"
api_key_env = "FAKE_API_KEY"
temperature = 0.1
""",
        encoding="utf-8",
    )
    pdf_texts = {
        "v1.pdf": SAMPLE_TEXT,
        "v2.pdf": SAMPLE_TEXT_V2,
    }
    monkeypatch.setattr(
        pipeline,
        "extract_pdf_lines",
        lambda path: [StyledTextLine(line) for line in pdf_texts[Path(path).name].splitlines()],
    )
    monkeypatch.setattr(pipeline, "LLMClient", lambda _settings: FakeLLM())

    first_plan = pipeline.generate(tmp_path / "v1.pdf", config_path=config)
    second_plan = pipeline.generate(tmp_path / "v2.pdf", config_path=config)
    repeated_plan = pipeline.generate(tmp_path / "v2.pdf", config_path=config)

    repo = pipeline.Repository(tmp_path / "db.sqlite")
    first_description = repo.get_description(first_plan.version)
    second_description = repo.get_description(second_plan.version)
    deltas = repo.get_deltas(second_plan.version)

    assert first_plan.version == "task_scheduler_with_dependencies_v1"
    assert second_plan.version == "task_scheduler_with_dependencies_v2"
    assert repeated_plan.version == second_plan.version
    assert first_description is not None
    assert first_description.project_name == "Task Scheduler with Dependencies"
    assert second_description is not None
    assert second_description.id is not None
    assert deltas is not None
    assert deltas.old_version == first_plan.version
    assert deltas.items[0].change_type == schemas.ChangeType.modified


def test_pipeline_auto_versions_with_explicit_project_name(
    tmp_path: Path,
    monkeypatch,
) -> None:
    config = tmp_path / "config.toml"
    config.write_text(
        f"""
[app]
database_path = "{tmp_path / "db.sqlite"}"
generated_dir = "{tmp_path / "generated"}"
reports_dir = "{tmp_path / "generated" / "reports"}"

[llm]
provider = "openai"
model_name = "fake-model"
api_key_env = "FAKE_API_KEY"
temperature = 0.1
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        pipeline,
        "extract_pdf_lines",
        lambda _path: [StyledTextLine(line) for line in SAMPLE_TEXT.splitlines()],
    )
    monkeypatch.setattr(pipeline, "LLMClient", lambda _settings: FakeLLM())

    plan = pipeline.generate(
        tmp_path / "input.pdf",
        config_path=config,
        project_name="Explicit Scheduler Project",
    )

    repo = pipeline.Repository(tmp_path / "db.sqlite")
    description = repo.get_description(plan.version)

    assert plan.version == "explicit_scheduler_project_v1"
    assert description is not None
    assert description.project_name == "Explicit Scheduler Project"


def test_pipeline_generate_rejects_none_provider(tmp_path: Path) -> None:
    config = tmp_path / "config.toml"
    config.write_text(
        """
[llm]
provider = "none"
""",
        encoding="utf-8",
    )

    with pytest.raises(RuntimeError, match='llm.provider is "none"'):
        pipeline.generate(tmp_path / "input.pdf", "v1", config_path=config)


def test_pipeline_generate_rejects_disabled_llm_toggle(tmp_path: Path) -> None:
    config = tmp_path / "config.toml"
    config.write_text(
        f"""
[app]
database_path = "{tmp_path / "db.sqlite"}"
generated_dir = "{tmp_path / "generated"}"
reports_dir = "{tmp_path / "generated" / "reports"}"

[llm]
provider = "openai"
model_name = "fake-model"
api_key_env = "FAKE_API_KEY"
use_llm_for_code = false
""",
        encoding="utf-8",
    )

    with pytest.raises(RuntimeError, match="disabled steps: code generation"):
        pipeline.generate(tmp_path / "input.pdf", "v1", config_path=config)
