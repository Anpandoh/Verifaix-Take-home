from __future__ import annotations

from pathlib import Path
from textwrap import shorten

from module_generator.config import load_settings
from module_generator.db import Repository
from module_generator.pipeline import (
    export_report,
    generate,
    init_database,
    run_tests,
    validate,
)


CONFIG_PATH = Path("config.toml")
PDF_V1 = Path("./Problem_Description_Software_Coding.pdf")
PDF_V2 = Path("./Problem_Description_Software_Coding_v2.pdf")
PROJECT_NAME = "Task Scheduler with Dependencies"
DELTA_DETAIL_WIDTH = 56


def main() -> None:
    settings = load_settings(CONFIG_PATH)
    repo = Repository(settings.app.database_path)

    print(f"Using database: {settings.app.database_path}")
    print(f"Using generated artifacts dir: {settings.app.generated_dir}")
    print(f"Using reports dir: {settings.app.reports_dir}")
    print(f"Using LLM: {settings.llm.provider} / {settings.llm.model_name}")

    init_database(CONFIG_PATH)

    version_v1 = run_module_generation(pdf_path=PDF_V1)
    version_v2 = run_module_generation(pdf_path=PDF_V2)

    delta_summary(repo, version_v2)
    output_locations(settings.app.reports_dir, settings.app.generated_dir, [version_v1, version_v2])


def run_module_generation(pdf_path: Path) -> str:
    print(f"\n=== Running {pdf_path} ===")
    plan = generate(pdf_path, config_path=CONFIG_PATH, project_name=PROJECT_NAME)
    version = plan.version
    print(f"Resolved version: {version}")
    print(f"Generated test plan: {len(plan.items)} items")

    results = run_tests(version, CONFIG_PATH)
    passed = sum(1 for result in results if result.status.value == "passed")
    print(f"Executed tests: {passed}/{len(results)} passed")

    report_dir = export_report(version, CONFIG_PATH)
    validation = validate(version, CONFIG_PATH)
    errors = sum(1 for issue in validation.issues if issue.severity.value == "error")
    warnings = sum(1 for issue in validation.issues if issue.severity.value == "warning")
    print(f"Validation issues: {errors} errors, {warnings} warnings")
    print(f"Report directory: {report_dir}")
    return version


def delta_summary(repo: Repository, version: str) -> None:
    deltas = repo.get_deltas(version)
    if deltas is None or not deltas.items:
        print(f"\nNo deltas found for {version}.")
        return

    print(f"\n=== Deltas for {version} ===")
    for item in deltas.items:
        detail = shorten(item.after or item.before or "", width=DELTA_DETAIL_WIDTH, placeholder="...")
        print(f"{item.id} {item.change_type.value.upper()} {item.item_id}: {detail}")


def output_locations(reports_dir: Path, generated_dir: Path, versions: list[str]) -> None:
    print("\n=== Key Outputs ===")
    for version in versions:
        print(f"{version} plan: {generated_dir / 'plans' / version / 'test_plan.json'}")
        print(f"{version} plan markdown: {generated_dir / 'plans' / version / 'test_plan.md'}")
        print(f"{version} code: {generated_dir / 'code' / version}")
        print(f"{version} tests: {generated_dir / 'tests' / version / 'test_generated.py'}")
        print(f"{version} results: {generated_dir / 'results' / version / 'execution_results.json'}")
        print(f"{version} validation: {reports_dir / version / 'validation_report.md'}")


if __name__ == "__main__":
    main()
