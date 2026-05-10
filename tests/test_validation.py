from pathlib import Path

from module_generator import schemas
from module_generator.db import Repository
from module_generator.utils import write_text
from module_generator.validation import render_validation_markdown, validate_version


def test_validate_version_builds_summary_traceability(tmp_path: Path) -> None:
    repo = Repository(tmp_path / "test.sqlite")
    version = "v1"
    repo.save_description(
        schemas.DescriptionVersion(
            version=version,
            pdf_path=tmp_path / "input.pdf",
            text_hash="abc",
            extracted_text="1. API\nDo thing",
        )
    )
    repo.save_test_plan(
        schemas.TestPlan(
            version=version,
            description_version=version,
            items=[
                schemas.TestPlanItem(
                    id="TP_1",
                    description="Module exposes callable",
                    source_sections=["1.1"],
                    expected_behavior="callable exists",
                ),
                schemas.TestPlanItem(
                    id="TP_10",
                    description="Later item",
                    source_sections=["1.2"],
                    expected_behavior="later behavior",
                ),
                schemas.TestPlanItem(
                    id="TP_2",
                    description="Second item",
                    source_sections=["1.2"],
                    expected_behavior="second behavior",
                )
            ],
        )
    )
    code_path = tmp_path / "generated" / "code" / version / "sample_module.py"
    tests_path = tmp_path / "generated" / "tests" / version / "test_generated.py"
    plan_path = tmp_path / "generated" / "plans" / version / "test_plan.json"
    results_path = tmp_path / "generated" / "results" / version / "execution_results.json"
    _save_artifact(
        repo,
        version,
        "generated_code",
        "sample_module.py",
        code_path,
        "def do_thing(value: bool) -> bool:\n"
        '    """Return the provided boolean value."""\n'
        "    return value\n",
    )
    _save_artifact(
        repo,
        version,
        "generated_tests",
        "test_generated.py",
        tests_path,
        "from sample_module import do_thing\n\n"
        "def test_tp_1_callable():\n"
        "    \"\"\"TP_1: callable exists.\"\"\"\n"
        "    assert do_thing(True) is True\n\n"
        "def test_tp_2_second_item():\n"
        "    \"\"\"TP_2: second behavior.\"\"\"\n"
        "    assert do_thing(True) is True\n\n"
        "def test_tp_10_later_item():\n"
        "    \"\"\"TP_10: later behavior.\"\"\"\n"
        "    assert do_thing(True) is True\n",
    )
    _save_artifact(repo, version, "test_plan", "test_plan.json", plan_path, "{}\n")
    _save_artifact(repo, version, "execution_results", "execution_results.json", results_path, "[]\n")
    repo.save_generated_code(
        schemas.GeneratedCodeRecord(
            version=version,
            module_name="sample_module",
            code_path=code_path,
        )
    )
    repo.save_generated_tests(
        [
            schemas.GeneratedTestRecord(
                version=version,
                test_name="test_tp_1_callable",
                test_plan_item_id="TP_1",
                code_path=tests_path,
            ),
            schemas.GeneratedTestRecord(
                version=version,
                test_name="test_tp_2_second_item",
                test_plan_item_id="TP_2",
                code_path=tests_path,
            ),
            schemas.GeneratedTestRecord(
                version=version,
                test_name="test_tp_10_later_item",
                test_plan_item_id="TP_10",
                code_path=tests_path,
            ),
        ]
    )
    repo.save_execution_results(
        [
            schemas.ExecutionResult(
                version=version,
                test_name="test_tp_1_callable",
                test_plan_item_ids=["TP_1"],
                status=schemas.TestStatus.passed,
            ),
            schemas.ExecutionResult(
                version=version,
                test_name="test_tp_2_second_item",
                test_plan_item_ids=["TP_2"],
                status=schemas.TestStatus.passed,
            ),
            schemas.ExecutionResult(
                version=version,
                test_name="test_tp_10_later_item",
                test_plan_item_ids=["TP_10"],
                status=schemas.TestStatus.passed,
            )
        ]
    )

    report = validate_version(version, repo)
    markdown = render_validation_markdown(report)

    assert report.summary["test_plan_items"] == 3
    assert [row.test_plan_id for row in report.traceability] == ["TP_1", "TP_2", "TP_10"]
    assert report.traceability[0].test_functions == ["test_tp_1_callable"]
    assert report.traceability[0].result_statuses == ["passed"]
    assert report.program_summary.module_name == "sample_module"
    assert report.program_summary.functions[0].parameters == ["value: bool"]
    assert report.program_summary.functions[0].returns == "bool"
    assert "Return the provided boolean value." in report.program_summary.behavior_summary
    assert report.summary["generated_code_records"] == 1
    assert report.summary["generated_test_records"] == 3
    assert report.delta_summary.items == []
    assert "## Generated Program Summary" in markdown
    assert "## Delta Summary" in markdown
    assert "No deltas are stored for this version." in markdown
    assert "## Traceability Matrix" in markdown
    assert "`TP_1`" in markdown


def test_validate_version_includes_delta_summary(tmp_path: Path) -> None:
    repo = Repository(tmp_path / "test.sqlite")
    repo.save_deltas(
        schemas.TestPlanDelta(
            old_version="v1",
            new_version="v2",
            items=[
                schemas.TestPlanDeltaItem(
                    id="D_10",
                    change_type=schemas.ChangeType.modified,
                    item_id="TP_2",
                    before="old behavior",
                    after="new behavior",
                ),
                schemas.TestPlanDeltaItem(
                    id="D_2",
                    change_type=schemas.ChangeType.added,
                    item_id="TP_10",
                    after="added behavior",
                ),
                schemas.TestPlanDeltaItem(
                    id="D_1",
                    change_type=schemas.ChangeType.removed,
                    item_id="TP_1",
                    before="removed behavior",
                ),
            ],
        )
    )

    report = validate_version("v2", repo)
    markdown = render_validation_markdown(report)

    assert report.delta_summary.old_version == "v1"
    assert report.delta_summary.new_version == "v2"
    assert report.delta_summary.added == 1
    assert report.delta_summary.removed == 1
    assert report.delta_summary.modified == 1
    assert [item.id for item in report.delta_summary.items] == ["D_1", "D_2", "D_10"]
    assert "Compared `v1` → `v2`: 1 added, 1 removed, 1 modified." in markdown
    assert "`D_10`" in markdown


def test_validate_version_reports_missing_test_coverage(tmp_path: Path) -> None:
    repo = Repository(tmp_path / "test.sqlite")
    version = "v1"
    repo.save_description(
        schemas.DescriptionVersion(
            version=version,
            pdf_path=tmp_path / "input.pdf",
            text_hash="abc",
            extracted_text="1. API\nDo thing",
        )
    )
    repo.save_test_plan(
        schemas.TestPlan(
            version=version,
            description_version=version,
            items=[
                schemas.TestPlanItem(
                    id="TP_1",
                    description="Module exposes callable",
                    source_sections=["1.1"],
                    expected_behavior="callable exists",
                )
            ],
        )
    )

    report = validate_version(version, repo)

    assert any(issue.check_name == "plan_item_has_test" for issue in report.issues)


def _save_artifact(
    repo: Repository,
    version: str,
    artifact_type: str,
    name: str,
    path: Path,
    content: str,
) -> None:
    content_hash = write_text(path, content)
    repo.save_artifact(
        schemas.ArtifactRecord(
            version=version,
            artifact_type=artifact_type,
            name=name,
            path=path,
            content_hash=content_hash,
        )
    )
