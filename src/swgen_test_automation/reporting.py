from __future__ import annotations

from pathlib import Path

from .database import Repository
from .utils import dumps_json, write_text


def export_report(version: str, repo: Repository, reports_dir: Path | str) -> Path:
    target = Path(reports_dir) / version
    target.mkdir(parents=True, exist_ok=True)

    plan = repo.get_test_plan(version)
    if plan is not None:
        write_text(target / "test_plan.json", dumps_json(plan.model_dump()))

    deltas = repo.get_deltas(version)
    if deltas is not None:
        write_text(target / "deltas.json", dumps_json(deltas.model_dump()))

    prompts = repo.get_prompts(version)
    write_text(target / "prompts.json", dumps_json([prompt.model_dump() for prompt in prompts]))

    artifacts = repo.get_artifacts(version)
    write_text(target / "artifacts.json", dumps_json([artifact.model_dump() for artifact in artifacts]))

    results = repo.get_execution_results(version)
    write_text(target / "execution_results.json", dumps_json([result.model_dump() for result in results]))

    return target
