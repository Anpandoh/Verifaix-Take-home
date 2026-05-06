from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field


class Section(BaseModel):
    id: str
    title: str
    text: str


class DescriptionVersion(BaseModel):
    version: str
    pdf_path: Path
    text_hash: str
    extracted_text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TestPlanItem(BaseModel):
    id: str
    description: str
    source_sections: list[str]
    test_type: str = "behavior"
    expected_behavior: str
    edge_case: bool = False


class TestPlan(BaseModel):
    version: str
    description_version: str
    items: list[TestPlanItem]
    summary: str = ""


class GeneratedModule(BaseModel):
    version: str
    module_name: str
    public_api: list[str]
    code: str
    source_sections: list[str] = Field(default_factory=list)
    test_plan_item_ids: list[str] = Field(default_factory=list)


class GeneratedTest(BaseModel):
    name: str
    test_plan_item_ids: list[str]
    code: str


class GeneratedTestSuite(BaseModel):
    version: str
    tests: list[GeneratedTest]

    def as_pytest_file(self) -> str:
        return "\n\n".join(test.code.rstrip() for test in self.tests) + "\n"


class ChangeType(StrEnum):
    added = "added"
    removed = "removed"
    modified = "modified"


class TestPlanDeltaItem(BaseModel):
    id: str
    change_type: ChangeType
    item_id: str
    before: str | None = None
    after: str | None = None


class TestPlanDelta(BaseModel):
    old_version: str
    new_version: str
    items: list[TestPlanDeltaItem]


class ArtifactRecord(BaseModel):
    version: str
    artifact_type: str
    name: str
    path: Path
    content_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TestStatus(StrEnum):
    passed = "passed"
    failed = "failed"
    error = "error"


class ExecutionResult(BaseModel):
    version: str
    test_name: str
    test_plan_item_ids: list[str]
    status: TestStatus
    failure_message: str | None = None
    duration_seconds: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PromptRecord(BaseModel):
    version: str
    prompt_type: str
    prompt_text: str
    provider: str
    model_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class GenerateRunRequest(BaseModel):
    pdf_path: Path
    version: str
    compare_to: str | None = None
    config_path: Path = Path("config.toml")


class TestRunRequest(BaseModel):
    version: str
    config_path: Path = Path("config.toml")
