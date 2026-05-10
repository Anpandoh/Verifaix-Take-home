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
    id: int | None = None
    project_name: str = "default"
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


class GeneratedCodeRecord(BaseModel):
    module_name: str
    version: str
    code_path: Path
    created_at: datetime = Field(default_factory=datetime.utcnow)


class GeneratedTestRecord(BaseModel):
    test_name: str
    test_plan_item_id: str
    version: str
    code_path: Path
    created_at: datetime = Field(default_factory=datetime.utcnow)


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


class GenerateRunRequest(BaseModel):
    pdf_path: Path
    version: str | None = None
    project_name: str | None = None
    compare_to: str | None = None
    config_path: Path = Path("config.toml")


class TestRunRequest(BaseModel):
    version: str
    config_path: Path = Path("config.toml")


class ValidationSeverity(StrEnum):
    info = "info"
    warning = "warning"
    error = "error"


class ValidationIssue(BaseModel):
    severity: ValidationSeverity
    check_name: str
    message: str


class TraceabilityRow(BaseModel):
    source_sections: list[str]
    test_plan_id: str
    requirement: str
    test_functions: list[str]
    result_statuses: list[str]


class ProgramFunctionSummary(BaseModel):
    name: str
    parameters: list[str]
    returns: str | None = None
    docstring: str | None = None
    raises: list[str] = Field(default_factory=list)


class ProgramSummary(BaseModel):
    module_name: str | None = None
    imports: list[str] = Field(default_factory=list)
    functions: list[ProgramFunctionSummary] = Field(default_factory=list)
    behavior_summary: str = "No generated code artifact was available to summarize."


class DeltaSummaryItem(BaseModel):
    id: str
    change_type: ChangeType
    item_id: str
    before: str | None = None
    after: str | None = None


class DeltaSummary(BaseModel):
    old_version: str | None = None
    new_version: str
    added: int = 0
    removed: int = 0
    modified: int = 0
    items: list[DeltaSummaryItem] = Field(default_factory=list)


class ValidationReport(BaseModel):
    version: str
    summary: dict[str, str | int | bool | None]
    program_summary: ProgramSummary
    delta_summary: DeltaSummary
    issues: list[ValidationIssue]
    traceability: list[TraceabilityRow]
