from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from module_generator import api
from module_generator import pipeline
from module_generator import schemas
from module_generator.db import Repository


def seeded_repo(tmp_path: Path) -> Repository:
    repo = Repository(tmp_path / "test.sqlite")
    repo.init_db()
    repo.save_description(
        schemas.DescriptionVersion(
            version="v1",
            pdf_path=tmp_path / "input.pdf",
            text_hash="abc",
            extracted_text="1. Overview\nText",
        )
    )
    repo.save_test_plan(
        schemas.TestPlan(
            version="v1",
            description_version="v1",
            summary="sample",
            items=[
                schemas.TestPlanItem(
                    id="TP_1",
                    description="Module exposes callable",
                    source_sections=["1.1"],
                    expected_behavior="callable exists",
                )
            ],
        )
    )
    code_path = tmp_path / "generated" / "code" / "v1" / "task_scheduler.py"
    tests_path = tmp_path / "generated" / "tests" / "v1" / "test_generated.py"
    repo.save_generated_code(
        schemas.GeneratedCodeRecord(
            module_name="task_scheduler",
            version="v1",
            code_path=code_path,
        )
    )
    repo.save_generated_tests(
        [
            schemas.GeneratedTestRecord(
                test_name="test_tp_1_callable",
                test_plan_item_id="TP_1",
                version="v1",
                code_path=tests_path,
            )
        ]
    )
    repo.save_deltas(
        schemas.TestPlanDelta(
            old_version="v1",
            new_version="v2",
            items=[
                schemas.TestPlanDeltaItem(
                    id="DELTA_1",
                    change_type=schemas.ChangeType.modified,
                    item_id="TP_1",
                    before="callable exists",
                    after="callable handles invalid inputs",
                )
            ],
        )
    )
    repo.save_execution_results(
        [
            schemas.ExecutionResult(
                version="v1",
                test_name="test_tp_1_callable",
                test_plan_item_ids=["TP_1"],
                status=schemas.TestStatus.passed,
                duration_seconds=0.01,
            )
        ]
    )
    return repo


def test_repository_and_api_return_openapi_backed_artifacts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = seeded_repo(tmp_path)

    generated_plan = schemas.TestPlan(
        version="v3",
        description_version="v3",
        summary="generated",
        items=[
            schemas.TestPlanItem(
                id="TP_2",
                description="Generated plan item",
                source_sections=["2.1"],
                expected_behavior="new behavior works",
            )
        ],
    )
    test_results = [
        schemas.ExecutionResult(
            version="v1",
            test_name="test_tp_1_callable",
            test_plan_item_ids=["TP_1"],
            status=schemas.TestStatus.passed,
            duration_seconds=0.02,
        )
    ]

    monkeypatch.setattr(pipeline, "generate", lambda *args, **kwargs: generated_plan)
    monkeypatch.setattr(pipeline, "run_tests", lambda *args, **kwargs: test_results)

    api.app.dependency_overrides[api.get_repo] = lambda: repo
    client = TestClient(api.app)
    try:
        assert client.get("/openapi.json").status_code == 200

        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["ok"] is True

        create_response = client.post(
            "/description-versions",
            json={
                "version": "v2",
                "pdf_path": str(tmp_path / "input_v2.pdf"),
                "text_hash": "def",
                "extracted_text": "2. Updated overview\nText",
            },
        )
        assert create_response.status_code == 200
        assert create_response.json()["version"] == "v2"

        description_response = client.get("/description-versions/v1")
        assert description_response.status_code == 200
        assert description_response.json()["text_hash"] == "abc"

        missing_description_response = client.get("/description-versions/missing")
        assert missing_description_response.status_code == 404

        response = client.get("/test-plans/v1")
        assert response.status_code == 200
        assert response.json()["items"][0]["id"] == "TP_1"

        missing_plan_response = client.get("/test-plans/missing")
        assert missing_plan_response.status_code == 404

        items_response = client.get("/test-plan-items/v1")
        assert items_response.status_code == 200
        assert items_response.json()[0]["expected_behavior"] == "callable exists"

        deltas_response = client.get("/deltas/v2")
        assert deltas_response.status_code == 200
        assert deltas_response.json()["items"][0]["change_type"] == "modified"

        missing_deltas_response = client.get("/deltas/missing")
        assert missing_deltas_response.status_code == 404

        code_response = client.get("/generated-code/v1")
        assert code_response.status_code == 200
        assert code_response.json()[0]["module_name"] == "task_scheduler"
        tests_response = client.get("/generated-tests/v1")
        assert tests_response.status_code == 200
        assert tests_response.json()[0]["test_plan_item_id"] == "TP_1"

        results_response = client.get("/execution-results/v1")
        assert results_response.status_code == 200
        assert results_response.json()[0]["status"] == "passed"

        generate_response = client.post(
            "/runs/generate",
            json={
                "pdf_path": str(tmp_path / "input_v3.pdf"),
                "version": "v3",
                "compare_to": "v1",
                "config_path": str(tmp_path / "config.toml"),
            },
        )
        assert generate_response.status_code == 200
        assert generate_response.json()["version"] == "v3"

        test_response = client.post(
            "/runs/test",
            json={
                "version": "v1",
                "config_path": str(tmp_path / "config.toml"),
            },
        )
        assert test_response.status_code == 200
        assert test_response.json()[0]["test_name"] == "test_tp_1_callable"
    finally:
        api.app.dependency_overrides.clear()
