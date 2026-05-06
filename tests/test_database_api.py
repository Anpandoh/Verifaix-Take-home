from pathlib import Path

from fastapi.testclient import TestClient

from swgen_test_automation import api
from swgen_test_automation import schemas
from swgen_test_automation.database import Repository


def test_repository_and_api_return_openapi_backed_artifacts(tmp_path: Path) -> None:
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

    api.app.dependency_overrides[api.get_repo] = lambda: repo
    client = TestClient(api.app)
    try:
        assert client.get("/openapi.json").status_code == 200
        response = client.get("/test-plans/v1")
        assert response.status_code == 200
        assert response.json()["items"][0]["id"] == "TP_1"
    finally:
        api.app.dependency_overrides.clear()
