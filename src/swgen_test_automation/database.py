from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .schemas import (
    ArtifactRecord,
    DescriptionVersion,
    ExecutionResult,
    PromptRecord,
    TestPlan,
    TestPlanDelta,
    TestPlanDeltaItem,
    TestPlanItem,
)
from .utils import ensure_parent


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS description_versions (
    version TEXT PRIMARY KEY,
    pdf_path TEXT NOT NULL,
    text_hash TEXT NOT NULL,
    extracted_text TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS test_plans (
    version TEXT PRIMARY KEY,
    description_version TEXT NOT NULL,
    summary TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(description_version) REFERENCES description_versions(version)
);

CREATE TABLE IF NOT EXISTS test_plan_items (
    version TEXT NOT NULL,
    item_id TEXT NOT NULL,
    description TEXT NOT NULL,
    source_sections TEXT NOT NULL,
    test_type TEXT NOT NULL,
    expected_behavior TEXT NOT NULL,
    edge_case INTEGER NOT NULL,
    PRIMARY KEY(version, item_id),
    FOREIGN KEY(version) REFERENCES test_plans(version)
);

CREATE TABLE IF NOT EXISTS test_plan_deltas (
    delta_id TEXT PRIMARY KEY,
    old_version TEXT NOT NULL,
    new_version TEXT NOT NULL,
    change_type TEXT NOT NULL,
    item_id TEXT NOT NULL,
    before_text TEXT,
    after_text TEXT
);

CREATE TABLE IF NOT EXISTS artifacts (
    version TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    name TEXT NOT NULL,
    path TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY(version, artifact_type, name)
);

CREATE TABLE IF NOT EXISTS execution_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version TEXT NOT NULL,
    test_name TEXT NOT NULL,
    test_plan_item_ids TEXT NOT NULL,
    status TEXT NOT NULL,
    failure_message TEXT,
    duration_seconds REAL NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version TEXT NOT NULL,
    prompt_type TEXT NOT NULL,
    prompt_text TEXT NOT NULL,
    provider TEXT NOT NULL,
    model_name TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class Repository:
    def __init__(self, db_path: Path | str):
        self.db_path = Path(db_path)

    def connect(self) -> sqlite3.Connection:
        ensure_parent(self.db_path)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def init_db(self) -> None:
        with self.connect() as conn:
            conn.executescript(SCHEMA)

    def health(self) -> dict[str, Any]:
        with self.connect() as conn:
            conn.execute("SELECT 1").fetchone()
        return {"ok": True, "database_path": str(self.db_path)}

    def save_description(self, description: DescriptionVersion) -> None:
        self.init_db()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO description_versions
                (version, pdf_path, text_hash, extracted_text, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    description.version,
                    str(description.pdf_path),
                    description.text_hash,
                    description.extracted_text,
                    description.created_at.isoformat(),
                ),
            )

    def get_description(self, version: str) -> DescriptionVersion | None:
        row = self._fetchone("SELECT * FROM description_versions WHERE version = ?", (version,))
        if not row:
            return None
        return DescriptionVersion(
            version=row["version"],
            pdf_path=Path(row["pdf_path"]),
            text_hash=row["text_hash"],
            extracted_text=row["extracted_text"],
            created_at=row["created_at"],
        )

    def save_test_plan(self, plan: TestPlan) -> None:
        self.init_db()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO test_plans (version, description_version, summary)
                VALUES (?, ?, ?)
                """,
                (plan.version, plan.description_version, plan.summary),
            )
            conn.execute("DELETE FROM test_plan_items WHERE version = ?", (plan.version,))
            conn.executemany(
                """
                INSERT INTO test_plan_items
                (version, item_id, description, source_sections, test_type, expected_behavior, edge_case)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        plan.version,
                        item.id,
                        item.description,
                        json.dumps(item.source_sections),
                        item.test_type,
                        item.expected_behavior,
                        int(item.edge_case),
                    )
                    for item in plan.items
                ],
            )

    def get_test_plan(self, version: str) -> TestPlan | None:
        plan_row = self._fetchone("SELECT * FROM test_plans WHERE version = ?", (version,))
        if not plan_row:
            return None
        return TestPlan(
            version=plan_row["version"],
            description_version=plan_row["description_version"],
            summary=plan_row["summary"],
            items=self.get_test_plan_items(version),
        )

    def get_test_plan_items(self, version: str) -> list[TestPlanItem]:
        rows = self._fetchall(
            "SELECT * FROM test_plan_items WHERE version = ? ORDER BY item_id",
            (version,),
        )
        return [
            TestPlanItem(
                id=row["item_id"],
                description=row["description"],
                source_sections=json.loads(row["source_sections"]),
                test_type=row["test_type"],
                expected_behavior=row["expected_behavior"],
                edge_case=bool(row["edge_case"]),
            )
            for row in rows
        ]

    def save_deltas(self, delta: TestPlanDelta) -> None:
        self.init_db()
        with self.connect() as conn:
            conn.execute("DELETE FROM test_plan_deltas WHERE new_version = ?", (delta.new_version,))
            conn.executemany(
                """
                INSERT INTO test_plan_deltas
                (delta_id, old_version, new_version, change_type, item_id, before_text, after_text)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        item.id,
                        delta.old_version,
                        delta.new_version,
                        item.change_type.value,
                        item.item_id,
                        item.before,
                        item.after,
                    )
                    for item in delta.items
                ],
            )

    def get_deltas(self, new_version: str) -> TestPlanDelta | None:
        rows = self._fetchall(
            "SELECT * FROM test_plan_deltas WHERE new_version = ? ORDER BY delta_id",
            (new_version,),
        )
        if not rows:
            return None
        return TestPlanDelta(
            old_version=rows[0]["old_version"],
            new_version=new_version,
            items=[
                TestPlanDeltaItem(
                    id=row["delta_id"],
                    change_type=row["change_type"],
                    item_id=row["item_id"],
                    before=row["before_text"],
                    after=row["after_text"],
                )
                for row in rows
            ],
        )

    def save_artifact(self, artifact: ArtifactRecord) -> None:
        self.init_db()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO artifacts
                (version, artifact_type, name, path, content_hash, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    artifact.version,
                    artifact.artifact_type,
                    artifact.name,
                    str(artifact.path),
                    artifact.content_hash,
                    artifact.created_at.isoformat(),
                ),
            )

    def get_artifacts(self, version: str, artifact_type: str | None = None) -> list[ArtifactRecord]:
        if artifact_type:
            rows = self._fetchall(
                "SELECT * FROM artifacts WHERE version = ? AND artifact_type = ? ORDER BY name",
                (version, artifact_type),
            )
        else:
            rows = self._fetchall(
                "SELECT * FROM artifacts WHERE version = ? ORDER BY artifact_type, name",
                (version,),
            )
        return [
            ArtifactRecord(
                version=row["version"],
                artifact_type=row["artifact_type"],
                name=row["name"],
                path=Path(row["path"]),
                content_hash=row["content_hash"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def save_execution_results(self, results: list[ExecutionResult]) -> None:
        self.init_db()
        if not results:
            return
        with self.connect() as conn:
            conn.executemany(
                """
                INSERT INTO execution_results
                (version, test_name, test_plan_item_ids, status, failure_message, duration_seconds, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        result.version,
                        result.test_name,
                        json.dumps(result.test_plan_item_ids),
                        result.status.value,
                        result.failure_message,
                        result.duration_seconds,
                        result.created_at.isoformat(),
                    )
                    for result in results
                ],
            )

    def get_execution_results(self, version: str) -> list[ExecutionResult]:
        rows = self._fetchall(
            "SELECT * FROM execution_results WHERE version = ? ORDER BY id",
            (version,),
        )
        return [
            ExecutionResult(
                version=row["version"],
                test_name=row["test_name"],
                test_plan_item_ids=json.loads(row["test_plan_item_ids"]),
                status=row["status"],
                failure_message=row["failure_message"],
                duration_seconds=row["duration_seconds"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def save_prompt(self, prompt: PromptRecord) -> None:
        self.init_db()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO prompts
                (version, prompt_type, prompt_text, provider, model_name, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    prompt.version,
                    prompt.prompt_type,
                    prompt.prompt_text,
                    prompt.provider,
                    prompt.model_name,
                    prompt.created_at.isoformat(),
                ),
            )

    def get_prompts(self, version: str) -> list[PromptRecord]:
        rows = self._fetchall("SELECT * FROM prompts WHERE version = ? ORDER BY id", (version,))
        return [
            PromptRecord(
                version=row["version"],
                prompt_type=row["prompt_type"],
                prompt_text=row["prompt_text"],
                provider=row["provider"],
                model_name=row["model_name"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def _fetchone(self, query: str, params: tuple[Any, ...]) -> sqlite3.Row | None:
        self.init_db()
        with self.connect() as conn:
            return conn.execute(query, params).fetchone()

    def _fetchall(self, query: str, params: tuple[Any, ...]) -> list[sqlite3.Row]:
        self.init_db()
        with self.connect() as conn:
            return list(conn.execute(query, params).fetchall())
