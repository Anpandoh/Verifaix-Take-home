from __future__ import annotations

import re
from collections.abc import Sequence
from pathlib import Path

from .config import LLMSettings, load_settings
from .db import Repository
from .delta import compare_test_plans
from .execute_tests import run_pytest_for_version
from .generation import Generators
from .ingestion import extract_pdf_lines, parse_sections, styled_lines_to_text
from .llm import LLMClient
from .schemas import (
    ArtifactRecord,
    DescriptionVersion,
    ExecutionResult,
    GeneratedCodeRecord,
    GeneratedModule,
    GeneratedTestRecord,
    GeneratedTestSuite,
    TestPlan,
    ValidationReport,
)
from .utils import dumps_json, sha256_text, write_text
from .validation import render_validation_markdown, validate_version

PROJECT_HEADER_RE = re.compile(
    r"^(?:problem|project|module)\s+description\s*:?\s*(?P<name>.+)?$",
    re.I,
)


def generate(
    pdf_path: Path | str,
    version: str | None = None,
    compare_to: str | None = None,
    config_path: Path | str = "config.toml",
    project_name: str | None = None,
) -> TestPlan:
    settings = load_settings(config_path)
    _require_llm_generation(settings.llm)
    repo = Repository(settings.app.database_path)
    repo.init_db()

    styled_lines = extract_pdf_lines(pdf_path)
    text = styled_lines_to_text(styled_lines)
    resolved_project_name = _resolve_project_name(project_name, styled_lines)
    text_hash = sha256_text(text)
    existing_description = repo.get_description_by_hash(resolved_project_name, text_hash)
    latest_description = repo.get_latest_description(resolved_project_name)
    resolved_version = version or (
        existing_description.version
        if existing_description is not None
        else _next_description_version(resolved_project_name, repo.count_descriptions(resolved_project_name))
    )

    if version is None and existing_description is not None:
        existing_plan = repo.get_test_plan(resolved_version)
        if existing_plan is not None:
            return existing_plan

    description = DescriptionVersion(
        project_name=resolved_project_name,
        version=resolved_version,
        pdf_path=Path(pdf_path),
        text_hash=text_hash,
        extracted_text=text,
    )
    repo.save_description(description)
    if (
        compare_to is None
        and latest_description is not None
        and latest_description.version != resolved_version
        and latest_description.text_hash != text_hash
    ):
        compare_to = latest_description.version

    sections = parse_sections(styled_lines)
    generators = Generators(LLMClient(settings.llm))

    test_plan, _ = generators.create_test_plan(resolved_version, description.version, sections)
    test_plan = test_plan.model_copy(
        update={"version": resolved_version, "description_version": description.version}
    )
    repo.save_test_plan(test_plan)
    _save_text_artifact(
        repo,
        resolved_version,
        "test_plan",
        "test_plan.json",
        settings.app.generated_dir / "plans" / resolved_version / "test_plan.json",
        dumps_json(test_plan.model_dump()),
    )

    generated_module, _ = generators.create_module(resolved_version, sections, test_plan)
    generated_module = generated_module.model_copy(update={"version": resolved_version})
    _write_module_artifact(repo, settings.app.generated_dir, generated_module)

    generated_tests, _ = generators.create_tests(
        resolved_version,
        sections,
        test_plan,
        generated_module,
    )
    generated_tests = generated_tests.model_copy(update={"version": resolved_version})
    _write_tests_artifact(repo, settings.app.generated_dir, generated_tests)

    if compare_to:
        old_plan = repo.get_test_plan(compare_to)
        if old_plan is None:
            raise ValueError(f"Cannot compare to missing test plan version {compare_to!r}")
        repo.save_deltas(compare_test_plans(old_plan, test_plan))

    return test_plan


def _resolve_project_name(
    project_name: str | None,
    styled_lines: Sequence[object],
) -> str:
    if project_name and project_name.strip():
        return project_name.strip()

    lines = [getattr(line, "text", str(line)).strip() for line in styled_lines]
    non_empty_lines = [line for line in lines if line]
    for index, line in enumerate(non_empty_lines[:10]):
        match = PROJECT_HEADER_RE.match(line)
        if match:
            header_name = (match.group("name") or "").strip()
            if header_name:
                return _join_wrapped_header_name(header_name, non_empty_lines, index + 1)
            if index + 1 < len(non_empty_lines):
                return non_empty_lines[index + 1]
        if index == 0:
            return line
    return "default"


def _join_wrapped_header_name(
    header_name: str,
    lines: list[str],
    next_index: int,
) -> str:
    parts = [header_name]
    for line in lines[next_index : next_index + 2]:
        if _looks_like_section_start(line):
            break
        if len(line.split()) > 4:
            break
        parts.append(line)
    return " ".join(parts)


def _looks_like_section_start(line: str) -> bool:
    return bool(re.match(r"^\d+(?:\.\d+)*\.?\s+", line))


def _next_description_version(project_name: str, existing_count: int) -> str:
    return f"{_slugify(project_name)}_v{existing_count + 1}"


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "project"


def _require_llm_generation(llm_settings: LLMSettings) -> None:
    disabled_steps = [
        step
        for step, enabled in [
            ("test plan generation", llm_settings.use_llm_for_testplan),
            ("code generation", llm_settings.use_llm_for_code),
            ("test generation", llm_settings.use_llm_for_tests),
        ]
        if not enabled
    ]
    if llm_settings.provider == "none" or disabled_steps:
        details = []
        if llm_settings.provider == "none":
            details.append('llm.provider is "none"')
        if disabled_steps:
            details.append(f"disabled steps: {', '.join(disabled_steps)}")
        raise RuntimeError(
            "This implementation requires a configured LLM for test-plan, code, and test "
            f"generation ({'; '.join(details)}). Set provider to 'openai' or 'anthropic' "
            "and keep use_llm_for_testplan, use_llm_for_code, and use_llm_for_tests enabled."
        )


def run_tests(
    version: str,
    config_path: Path | str = "config.toml",
) -> list[ExecutionResult]:
    settings = load_settings(config_path)
    repo = Repository(settings.app.database_path)
    results = run_pytest_for_version(version, settings.app.generated_dir)
    repo.save_execution_results(results)
    _save_text_artifact(
        repo,
        version,
        "execution_results",
        "execution_results.json",
        settings.app.generated_dir / "results" / version / "execution_results.json",
        dumps_json([result.model_dump() for result in results]),
    )
    return results


def export_report(
    version: str,
    config_path: Path | str = "config.toml",
) -> Path:
    settings = load_settings(config_path)
    repo = Repository(settings.app.database_path)
    target = settings.app.reports_dir / version
    target.mkdir(parents=True, exist_ok=True)

    plan = repo.get_test_plan(version)
    if plan is not None:
        write_text(target / "test_plan.json", dumps_json(plan.model_dump()))

    deltas = repo.get_deltas(version)
    if deltas is not None:
        write_text(target / "deltas.json", dumps_json(deltas.model_dump()))

    generated_code = repo.get_generated_code(version)
    write_text(
        target / "generated_code.json",
        dumps_json([record.model_dump() for record in generated_code]),
    )

    generated_tests = repo.get_generated_tests(version)
    write_text(
        target / "generated_tests.json",
        dumps_json([record.model_dump() for record in generated_tests]),
    )

    artifacts = repo.get_artifacts(version)
    write_text(target / "artifacts.json", dumps_json([artifact.model_dump() for artifact in artifacts]))

    results = repo.get_execution_results(version)
    write_text(target / "execution_results.json", dumps_json([result.model_dump() for result in results]))

    return target


def validate(
    version: str,
    config_path: Path | str = "config.toml",
) -> ValidationReport:
    settings = load_settings(config_path)
    repo = Repository(settings.app.database_path)
    report = validate_version(version, repo)
    markdown = render_validation_markdown(report)
    report_path = settings.app.reports_dir / version / "validation_report.md"
    json_path = settings.app.reports_dir / version / "validation_report.json"
    write_text(report_path, markdown)
    write_text(json_path, dumps_json(report.model_dump()))
    return report


def init_database(config_path: Path | str = "config.toml") -> None:
    settings = load_settings(config_path)
    Repository(settings.app.database_path).init_db()


def _write_module_artifact(
    repo: Repository,
    generated_dir: Path,
    generated_module: GeneratedModule,
) -> None:
    path = generated_dir / "code" / generated_module.version / f"{generated_module.module_name}.py"
    repo.save_generated_code(
        GeneratedCodeRecord(
            version=generated_module.version,
            module_name=generated_module.module_name,
            code_path=path,
        )
    )
    _save_text_artifact(
        repo,
        generated_module.version,
        "generated_code",
        f"{generated_module.module_name}.py",
        path,
        generated_module.code.rstrip() + "\n",
    )


def _write_tests_artifact(
    repo: Repository,
    generated_dir: Path,
    generated_tests: GeneratedTestSuite,
) -> None:
    path = generated_dir / "tests" / generated_tests.version / "test_generated.py"
    repo.save_generated_tests(
        [
            GeneratedTestRecord(
                version=generated_tests.version,
                test_name=test.name,
                test_plan_item_id=test_plan_item_id,
                code_path=path,
            )
            for test in generated_tests.tests
            for test_plan_item_id in test.test_plan_item_ids
        ]
    )
    _save_text_artifact(
        repo,
        generated_tests.version,
        "generated_tests",
        "test_generated.py",
        path,
        generated_tests.as_pytest_file(),
    )


def _save_text_artifact(
    repo: Repository,
    version: str,
    artifact_type: str,
    name: str,
    path: Path,
    content: str,
) -> None:
    content_hash = write_text(path, content)
    repo.save_artifact(
        ArtifactRecord(
            version=version,
            artifact_type=artifact_type,
            name=name,
            path=path,
            content_hash=content_hash,
        )
    )

