from __future__ import annotations

from pathlib import Path

from .config import load_settings
from .database import Repository
from .delta import compare_test_plans
from .generators import Generators
from .llm_client import LLMClient
from .pdf_reader import extract_pdf_text
from .reporting import export_report as export_report_files
from .runner import run_pytest_for_version
from .schemas import (
    ArtifactRecord,
    DescriptionVersion,
    ExecutionResult,
    GeneratedModule,
    GeneratedTestSuite,
    PromptRecord,
    TestPlan,
)
from .section_parser import parse_sections
from .utils import dumps_json, sha256_text, write_text


def generate(
    pdf_path: Path | str,
    version: str,
    compare_to: str | None = None,
    config_path: Path | str = "config.toml",
) -> TestPlan:
    settings = load_settings(config_path)
    repo = Repository(settings.app.database_path)
    repo.init_db()

    text = extract_pdf_text(pdf_path)
    description = DescriptionVersion(
        version=version,
        pdf_path=Path(pdf_path),
        text_hash=sha256_text(text),
        extracted_text=text,
    )
    repo.save_description(description)

    sections = parse_sections(text)
    generators = Generators(LLMClient(settings.llm))

    test_plan, plan_prompt = generators.create_test_plan(version, version, sections)
    repo.save_prompt(_prompt(version, "test_plan", plan_prompt, settings.llm.provider, settings.llm.model_name))
    repo.save_test_plan(test_plan)
    _save_text_artifact(
        repo,
        version,
        "test_plan",
        "test_plan.json",
        settings.app.generated_dir / "plans" / version / "test_plan.json",
        dumps_json(test_plan.model_dump()),
    )

    generated_module, code_prompt = generators.create_module(version, sections, test_plan)
    repo.save_prompt(_prompt(version, "code", code_prompt, settings.llm.provider, settings.llm.model_name))
    _write_module_artifact(repo, settings.app.generated_dir, generated_module)

    generated_tests, tests_prompt = generators.create_tests(
        version,
        sections,
        test_plan,
        generated_module,
    )
    repo.save_prompt(_prompt(version, "tests", tests_prompt, settings.llm.provider, settings.llm.model_name))
    _write_tests_artifact(repo, settings.app.generated_dir, generated_tests)

    if compare_to:
        old_plan = repo.get_test_plan(compare_to)
        if old_plan is None:
            raise ValueError(f"Cannot compare to missing test plan version {compare_to!r}")
        repo.save_deltas(compare_test_plans(old_plan, test_plan))

    return test_plan


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
    return export_report_files(version, repo, settings.app.reports_dir)


def init_database(config_path: Path | str = "config.toml") -> None:
    settings = load_settings(config_path)
    Repository(settings.app.database_path).init_db()


def _write_module_artifact(
    repo: Repository,
    generated_dir: Path,
    generated_module: GeneratedModule,
) -> None:
    path = generated_dir / "code" / generated_module.version / f"{generated_module.module_name}.py"
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


def _prompt(
    version: str,
    prompt_type: str,
    prompt_text: str,
    provider: str,
    model_name: str,
) -> PromptRecord:
    return PromptRecord(
        version=version,
        prompt_type=prompt_type,
        prompt_text=prompt_text,
        provider=provider,
        model_name=model_name,
    )
