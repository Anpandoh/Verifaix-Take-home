from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException

from .config import load_settings
from .database import Repository
from .schemas import (
    ArtifactRecord,
    DescriptionVersion,
    ExecutionResult,
    GenerateRunRequest,
    TestPlan,
    TestPlanDelta,
    TestPlanItem,
    TestRunRequest,
)

app = FastAPI(
    title="Software Generation and Testing Automation",
    version="0.1.0",
    description="CRUD/read API for generated plans, code, tests, deltas, and results.",
)


def get_repo() -> Repository:
    settings = load_settings()
    return Repository(settings.app.database_path)


@app.get("/health")
def health(repo: Repository = Depends(get_repo)) -> dict[str, object]:
    return repo.health()


@app.post("/description-versions", response_model=DescriptionVersion)
def create_description(
    description: DescriptionVersion,
    repo: Repository = Depends(get_repo),
) -> DescriptionVersion:
    repo.save_description(description)
    return description


@app.get("/description-versions/{version}", response_model=DescriptionVersion)
def get_description(version: str, repo: Repository = Depends(get_repo)) -> DescriptionVersion:
    description = repo.get_description(version)
    if description is None:
        raise HTTPException(status_code=404, detail="Description version not found")
    return description


@app.get("/test-plans/{version}", response_model=TestPlan)
def get_test_plan(version: str, repo: Repository = Depends(get_repo)) -> TestPlan:
    plan = repo.get_test_plan(version)
    if plan is None:
        raise HTTPException(status_code=404, detail="Test plan not found")
    return plan


@app.get("/test-plan-items/{version}", response_model=list[TestPlanItem])
def get_test_plan_items(version: str, repo: Repository = Depends(get_repo)) -> list[TestPlanItem]:
    return repo.get_test_plan_items(version)


@app.get("/deltas/{new_version}", response_model=TestPlanDelta)
def get_deltas(new_version: str, repo: Repository = Depends(get_repo)) -> TestPlanDelta:
    deltas = repo.get_deltas(new_version)
    if deltas is None:
        raise HTTPException(status_code=404, detail="Deltas not found")
    return deltas


@app.get("/generated-code/{version}", response_model=list[ArtifactRecord])
def get_generated_code(version: str, repo: Repository = Depends(get_repo)) -> list[ArtifactRecord]:
    return repo.get_artifacts(version, "generated_code")


@app.get("/generated-tests/{version}", response_model=list[ArtifactRecord])
def get_generated_tests(version: str, repo: Repository = Depends(get_repo)) -> list[ArtifactRecord]:
    return repo.get_artifacts(version, "generated_tests")


@app.get("/execution-results/{version}", response_model=list[ExecutionResult])
def get_execution_results(
    version: str,
    repo: Repository = Depends(get_repo),
) -> list[ExecutionResult]:
    return repo.get_execution_results(version)


@app.post("/runs/generate", response_model=TestPlan)
def generate_run(request: GenerateRunRequest) -> TestPlan:
    from .pipeline import generate

    return generate(request.pdf_path, request.version, request.compare_to, request.config_path)


@app.post("/runs/test", response_model=list[ExecutionResult])
def test_run(request: TestRunRequest) -> list[ExecutionResult]:
    from .pipeline import run_tests

    return run_tests(request.version, request.config_path)
