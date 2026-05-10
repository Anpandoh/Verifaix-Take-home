from module_generator.ingestion import StyledTextLine, parse_sections


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


def test_parse_sections_extracts_unnumbered_headings() -> None:
    text = """Problem Description
Overview
Module text
Error Handling
Invalid input raises ValueError
"""

    sections = parse_sections(text)

    assert [section.id for section in sections] == ["0", "section_1", "section_2"]
    assert sections[1].title == "Overview"
    assert sections[2].title == "Error Handling"


def test_parse_sections_uses_styled_pdf_lines_as_heading_hints() -> None:
    lines = [
        StyledTextLine("Problem Description", font_size=16, font_name="Helvetica-Bold"),
        StyledTextLine("Module text", font_size=10, font_name="Helvetica"),
        StyledTextLine("Ordering Rules", font_size=14, font_name="Helvetica-Bold"),
        StyledTextLine("Every task appears once", font_size=10, font_name="Helvetica"),
        StyledTextLine("Validation", font_size=10, font_name="Helvetica", color="rgb:0.000,0.000,1.000"),
        StyledTextLine("Bad inputs fail", font_size=10, font_name="Helvetica"),
    ]

    sections = parse_sections(lines)

    assert [section.id for section in sections] == ["section_1", "section_2", "section_3"]
    assert sections[0].title == "Problem Description"
    assert sections[1].title == "Ordering Rules"
    assert sections[2].title == "Validation"
