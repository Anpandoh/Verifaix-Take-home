from pathlib import Path

from swgen_test_automation import schemas
from swgen_test_automation import pipeline


SAMPLE_TEXT = """Problem Description: Task Scheduler with Dependencies
1. Overview
A Python module that computes a valid execution order for tasks with dependencies.
1.1 API
schedule_tasks(tasks: list[str], dependencies: list[tuple[str, str]]) -> list[str]
1.2 Ordering Rules
Every task appears exactly once.
"""


class FakeLLM:
    def generate_model(self, _prompt: str, model_type: type):
        if model_type is schemas.TestPlan:
            return schemas.TestPlan(
                version="v1",
                description_version="v1",
                summary="Scheduler plan",
                items=[
                    schemas.TestPlanItem(
                        id="TP_1",
                        description="Module exposes schedule_tasks",
                        source_sections=["1.1"],
                        expected_behavior="callable is present",
                    )
                ],
            )
        if model_type is schemas.GeneratedModule:
            return schemas.GeneratedModule(
                version="v1",
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
                version="v1",
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
reports_dir = "{tmp_path / "reports"}"

[llm]
provider = "openai"
model_name = "fake-model"
api_key_env = "FAKE_API_KEY"
temperature = 0.1
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(pipeline, "extract_pdf_text", lambda _path: SAMPLE_TEXT)
    monkeypatch.setattr(pipeline, "LLMClient", lambda _settings: FakeLLM())

    plan = pipeline.generate(tmp_path / "input.pdf", "v1", config_path=config)
    results = pipeline.run_tests("v1", config_path=config)
    report_path = pipeline.export_report("v1", config_path=config)

    assert plan.items[0].id == "TP_1"
    assert results[0].status.value == "passed"
    assert (tmp_path / "generated" / "code" / "v1" / "task_scheduler.py").exists()
    assert (report_path / "test_plan.json").exists()
