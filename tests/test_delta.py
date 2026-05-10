from module_generator.delta import compare_test_plans
from module_generator import schemas


def _item(item_id: str, description: str) -> schemas.TestPlanItem:
    return schemas.TestPlanItem(
        id=item_id,
        description=description,
        source_sections=["1.1"],
        expected_behavior=description,
    )


def test_compare_test_plans_detects_added_removed_and_modified_items() -> None:
    old = schemas.TestPlan(
        version="v1",
        description_version="v1",
        items=[_item("TP_1", "old"), _item("TP_2", "remove")],
    )
    new = schemas.TestPlan(
        version="v2",
        description_version="v2",
        items=[_item("TP_1", "new"), _item("TP_3", "add")],
    )

    delta = compare_test_plans(old, new)

    assert [(item.change_type.value, item.item_id) for item in delta.items] == [
        ("added", "TP_3"),
        ("removed", "TP_2"),
        ("modified", "TP_1"),
    ]
