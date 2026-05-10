from __future__ import annotations

from .schemas import ChangeType, TestPlan, TestPlanDelta, TestPlanDeltaItem, TestPlanItem


def compare_test_plans(old: TestPlan, new: TestPlan) -> TestPlanDelta:
    old_items = {item.id: item for item in old.items}
    new_items = {item.id: item for item in new.items}
    deltas: list[TestPlanDeltaItem] = []
    counter = 1

    for item_id in sorted(new_items.keys() - old_items.keys()):
        item = new_items[item_id]
        deltas.append(
            TestPlanDeltaItem(
                id=f"D_{counter}",
                change_type=ChangeType.added,
                item_id=item_id,
                after=_summarize_item(item),
            )
        )
        counter += 1

    for item_id in sorted(old_items.keys() - new_items.keys()):
        item = old_items[item_id]
        deltas.append(
            TestPlanDeltaItem(
                id=f"D_{counter}",
                change_type=ChangeType.removed,
                item_id=item_id,
                before=_summarize_item(item),
            )
        )
        counter += 1

    for item_id in sorted(old_items.keys() & new_items.keys()):
        old_summary = _summarize_item(old_items[item_id])
        new_summary = _summarize_item(new_items[item_id])
        if old_summary != new_summary:
            deltas.append(
                TestPlanDeltaItem(
                    id=f"D_{counter}",
                    change_type=ChangeType.modified,
                    item_id=item_id,
                    before=old_summary,
                    after=new_summary,
                )
            )
            counter += 1

    return TestPlanDelta(old_version=old.version, new_version=new.version, items=deltas)


def _summarize_item(item: TestPlanItem) -> str:
    sections = ", ".join(item.source_sections)
    return (
        f"{item.description} | sections={sections} | "
        f"type={item.test_type} | expected={item.expected_behavior} | edge={item.edge_case}"
    )
