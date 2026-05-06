from pathlib import Path

from swgen_test_automation.runner import run_pytest_for_version


def test_runner_maps_pytest_results_to_test_plan_ids(tmp_path: Path) -> None:
    code_dir = tmp_path / "code" / "v1"
    tests_dir = tmp_path / "tests" / "v1"
    code_dir.mkdir(parents=True)
    tests_dir.mkdir(parents=True)
    (code_dir / "sample_module.py").write_text(
        "def add_one(value: int) -> int:\n    return value + 1\n",
        encoding="utf-8",
    )
    (tests_dir / "test_generated.py").write_text(
        "from sample_module import add_one\n\n"
        "def test_tp_1_add_one():\n"
        "    \"\"\"TP_1: add one.\"\"\"\n"
        "    assert add_one(1) == 2\n",
        encoding="utf-8",
    )

    results = run_pytest_for_version("v1", tmp_path)

    assert len(results) == 1
    assert results[0].status.value == "passed"
    assert results[0].test_plan_item_ids == ["TP_1"]
