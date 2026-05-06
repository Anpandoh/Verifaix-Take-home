from __future__ import annotations

import re

from .schemas import Section

SECTION_RE = re.compile(r"^(?P<id>\d+(?:\.\d+)*)(?:\.)?\s+(?P<title>.+)$")


def parse_sections(text: str) -> list[Section]:
    sections: list[Section] = []
    current_id = "0"
    current_title = "Document"
    current_lines: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = SECTION_RE.match(line)
        if match:
            _append_section(sections, current_id, current_title, current_lines)
            current_id = match.group("id")
            current_title = match.group("title").strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    _append_section(sections, current_id, current_title, current_lines)
    return sections


def _append_section(
    sections: list[Section],
    section_id: str,
    title: str,
    lines: list[str],
) -> None:
    text = "\n".join(lines).strip()
    if text:
        sections.append(Section(id=section_id, title=title, text=text))
