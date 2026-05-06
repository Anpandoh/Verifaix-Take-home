from swgen_test_automation.section_parser import parse_sections


def test_parse_sections_extracts_numbered_sections() -> None:
    text = """Problem Description
1. Overview
Module text
1.1 API
schedule_tasks(...)
1.2 Ordering Rules
Every task appears once
"""

    sections = parse_sections(text)

    assert [section.id for section in sections] == ["0", "1", "1.1", "1.2"]
    assert sections[2].title == "API"
    assert "schedule_tasks" in sections[2].text
