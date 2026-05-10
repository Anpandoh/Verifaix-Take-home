from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from ..schemas import (
    ArtifactRecord,
    DescriptionVersion,
    ExecutionResult,
    GeneratedCodeRecord,
    GeneratedTestRecord,
    TestPlan,
    TestPlanDelta,
    TestPlanDeltaItem,
    TestPlanItem,
)
from ..utils import ensure_parent

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


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
            conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
            self._migrate_description_versions(conn)
            self._migrate_test_plan_deltas(conn)

    def health(self) -> dict[str, Any]:
        with self.connect() as conn:
            conn.execute("SELECT 1").fetchone()
        return {"ok": True, "database_path": str(self.db_path)}

    def save_description(self, description: DescriptionVersion) -> None:
        self.init_db()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO description_versions
                (project_name, version, pdf_path, text_hash, extracted_text, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(version) DO UPDATE SET
                    project_name = excluded.project_name,
                    pdf_path = excluded.pdf_path,
                    text_hash = excluded.text_hash,
                    extracted_text = excluded.extracted_text,
                    created_at = excluded.created_at
                """,
                (
                    description.project_name,
                    description.version,
                    str(description.pdf_path),
                    description.text_hash,
                    description.extracted_text,
                    description.created_at.isoformat(),
                ),
            )

    def get_description(self, version: str) -> DescriptionVersion | None:
        row = self._fetchone(
            "SELECT rowid AS row_id, * FROM description_versions WHERE version = ?",
            (version,),
        )
        if not row:
            return None
        return self._description_from_row(row)

    def get_description_by_hash(
        self,
        project_name: str,
        text_hash: str,
    ) -> DescriptionVersion | None:
        row = self._fetchone(
            """
            SELECT rowid AS row_id, * FROM description_versions
            WHERE project_name = ? AND text_hash = ?
            ORDER BY created_at DESC, rowid DESC
            LIMIT 1
            """,
            (project_name, text_hash),
        )
        if not row:
            return None
        return self._description_from_row(row)

    def get_latest_description(self, project_name: str) -> DescriptionVersion | None:
        row = self._fetchone(
            """
            SELECT rowid AS row_id, * FROM description_versions
            WHERE project_name = ?
            ORDER BY created_at DESC, rowid DESC
            LIMIT 1
            """,
            (project_name,),
        )
        if not row:
            return None
        return self._description_from_row(row)

    def count_descriptions(self, project_name: str) -> int:
        row = self._fetchone(
            "SELECT COUNT(*) AS count FROM description_versions WHERE project_name = ?",
            (project_name,),
        )
        return int(row["count"]) if row else 0

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

    def save_generated_code(self, record: GeneratedCodeRecord) -> None:
        self.init_db()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO generated_code
                (version, module_name, code_path, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    record.version,
                    record.module_name,
                    str(record.code_path),
                    record.created_at.isoformat(),
                ),
            )

    def get_generated_code(self, version: str) -> list[GeneratedCodeRecord]:
        rows = self._fetchall(
            "SELECT * FROM generated_code WHERE version = ? ORDER BY module_name",
            (version,),
        )
        return [
            GeneratedCodeRecord(
                version=row["version"],
                module_name=row["module_name"],
                code_path=Path(row["code_path"]),
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def save_generated_tests(self, records: list[GeneratedTestRecord]) -> None:
        self.init_db()
        if not records:
            return
        version = records[0].version
        with self.connect() as conn:
            conn.execute("DELETE FROM generated_tests WHERE version = ?", (version,))
            conn.executemany(
                """
                INSERT INTO generated_tests
                (version, test_name, test_plan_item_id, code_path, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (
                        record.version,
                        record.test_name,
                        record.test_plan_item_id,
                        str(record.code_path),
                        record.created_at.isoformat(),
                    )
                    for record in records
                ],
            )

    def get_generated_tests(self, version: str) -> list[GeneratedTestRecord]:
        rows = self._fetchall(
            """
            SELECT * FROM generated_tests
            WHERE version = ?
            ORDER BY test_name, test_plan_item_id
            """,
            (version,),
        )
        return [
            GeneratedTestRecord(
                version=row["version"],
                test_name=row["test_name"],
                test_plan_item_id=row["test_plan_item_id"],
                code_path=Path(row["code_path"]),
                created_at=row["created_at"],
            )
            for row in rows
        ]

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

    def _fetchone(self, query: str, params: tuple[Any, ...]) -> sqlite3.Row | None:
        self.init_db()
        with self.connect() as conn:
            return conn.execute(query, params).fetchone()

    def _fetchall(self, query: str, params: tuple[Any, ...]) -> list[sqlite3.Row]:
        self.init_db()
        with self.connect() as conn:
            return list(conn.execute(query, params).fetchall())

    def _migrate_description_versions(self, conn: sqlite3.Connection) -> None:
        columns = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(description_versions)").fetchall()
        }
        if "project_name" not in columns:
            conn.execute(
                "ALTER TABLE description_versions "
                "ADD COLUMN project_name TEXT NOT NULL DEFAULT 'default'"
            )

    def _migrate_test_plan_deltas(self, conn: sqlite3.Connection) -> None:
        table_info = conn.execute("PRAGMA table_info(test_plan_deltas)").fetchall()
        delta_id_info = next((row for row in table_info if row["name"] == "delta_id"), None)
        if delta_id_info is None or delta_id_info["pk"] != 1:
            return

        conn.execute("ALTER TABLE test_plan_deltas RENAME TO test_plan_deltas_old")
        conn.execute(
            """
            CREATE TABLE test_plan_deltas (
                delta_id TEXT NOT NULL,
                old_version TEXT NOT NULL,
                new_version TEXT NOT NULL,
                change_type TEXT NOT NULL,
                item_id TEXT NOT NULL,
                before_text TEXT,
                after_text TEXT,
                PRIMARY KEY(new_version, delta_id)
            )
            """
        )
        conn.execute(
            """
            INSERT OR IGNORE INTO test_plan_deltas
            (delta_id, old_version, new_version, change_type, item_id, before_text, after_text)
            SELECT delta_id, old_version, new_version, change_type, item_id, before_text, after_text
            FROM test_plan_deltas_old
            """
        )
        conn.execute("DROP TABLE test_plan_deltas_old")

    def _description_from_row(self, row: sqlite3.Row) -> DescriptionVersion:
        keys = set(row.keys())
        description_id = row["id"] if "id" in keys else row["row_id"]
        return DescriptionVersion(
            id=description_id,
            project_name=row["project_name"],
            version=row["version"],
            pdf_path=Path(row["pdf_path"]),
            text_hash=row["text_hash"],
            extracted_text=row["extracted_text"],
            created_at=row["created_at"],
        )
