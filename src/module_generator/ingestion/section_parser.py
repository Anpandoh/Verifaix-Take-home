from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from statistics import median

from ..schemas import Section

SECTION_RE = re.compile(r"^(?P<id>\d+(?:\.\d+)*)(?:\.)?\s+(?P<title>.+)$")
APPENDIX_RE = re.compile(r"^(?P<id>appendix[-_ ]?[A-Z0-9]+)(?:[.:])?\s*(?P<title>.*)$", re.I)
KNOWN_HEADING_RE = re.compile(
    r"^(overview|requirements?|constraints?|assumptions?|examples?|api|inputs?|outputs?|"
    r"error handling|edge cases?|ordering rules?|validation|configuration|usage)$",
    re.I,
)
SENTENCE_ENDINGS = (".", ",", ";")


@dataclass(frozen=True)
class StyledTextLine:
    text: str
    font_size: float | None = None
    font_name: str | None = None
    color: str | None = None


def parse_sections(text: str | Sequence[StyledTextLine]) -> list[Section]:
    lines = _coerce_lines(text)
    body_font_size = _body_font_size(lines)
    body_color = _body_color(lines)
    sections: list[Section] = []
    current_id = "0"
    current_title = "Document"
    current_lines: list[str] = []
    synthetic_id = 1

    for styled_line in lines:
        line = styled_line.text.strip()
        if not line:
            continue
        heading = _detect_heading(
            styled_line,
            body_font_size,
            body_color,
            allow_plain_title=bool(current_lines),
        )
        if heading:
            _append_section(sections, current_id, current_title, current_lines)
            heading_id, heading_title = heading
            if heading_id is None:
                heading_id = f"section_{synthetic_id}"
                synthetic_id += 1
            current_id = heading_id
            current_title = heading_title
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


def _coerce_lines(text: str | Sequence[StyledTextLine]) -> list[StyledTextLine]:
    if isinstance(text, str):
        return [StyledTextLine(line) for line in text.splitlines()]
    return list(text)


def _detect_heading(
    line: StyledTextLine,
    body_font_size: float | None,
    body_color: str | None,
    *,
    allow_plain_title: bool,
) -> tuple[str | None, str] | None:
    text = line.text.strip()
    numbered_match = SECTION_RE.match(text)
    if numbered_match:
        return numbered_match.group("id"), numbered_match.group("title").strip()

    appendix_match = APPENDIX_RE.match(text)
    if appendix_match:
        heading_id = appendix_match.group("id").replace(" ", "_").replace("-", "_").lower()
        title = appendix_match.group("title").strip() or text
        return heading_id, title

    if not _can_be_heading_text(text):
        return None

    if _has_style_heading_cue(line, body_font_size, body_color):
        return None, text

    if KNOWN_HEADING_RE.match(text):
        return None, text

    if allow_plain_title and (_is_strong_title_case(text) or _is_all_caps_heading(text)):
        return None, text

    return None


def _can_be_heading_text(text: str) -> bool:
    words = text.split()
    if not words or len(words) > 8 or len(text) > 90:
        return False
    if text.endswith(SENTENCE_ENDINGS):
        return False
    if text.startswith(("-", "*", "•")):
        return False
    return True


def _has_style_heading_cue(
    line: StyledTextLine,
    body_font_size: float | None,
    body_color: str | None,
) -> bool:
    larger_font = (
        body_font_size is not None
        and line.font_size is not None
        and line.font_size >= body_font_size * 1.12
    )
    bold_font = line.font_name is not None and "bold" in line.font_name.lower()
    different_color = body_color is not None and line.color is not None and line.color != body_color
    return larger_font or bold_font or (different_color and (_is_strong_title_case(line.text) or bold_font))


def _body_font_size(lines: Sequence[StyledTextLine]) -> float | None:
    sizes = [line.font_size for line in lines if line.text.strip() and line.font_size is not None]
    if not sizes:
        return None
    return median(sizes)


def _body_color(lines: Sequence[StyledTextLine]) -> str | None:
    colors = [line.color for line in lines if line.text.strip() and line.color is not None]
    if not colors:
        return None
    return max(set(colors), key=colors.count)


def _is_strong_title_case(text: str) -> bool:
    words = [word.strip("()[]{}") for word in text.split()]
    significant_words = [word for word in words if len(word) > 2]
    if len(significant_words) < 2:
        return False
    return all(word[:1].isupper() for word in significant_words if word[:1].isalpha())


def _is_all_caps_heading(text: str) -> bool:
    letters = [char for char in text if char.isalpha()]
    return bool(letters) and sum(char.isupper() for char in letters) / len(letters) >= 0.8
