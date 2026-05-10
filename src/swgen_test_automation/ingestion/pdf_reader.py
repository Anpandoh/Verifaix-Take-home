from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from pypdf import PdfReader

from ..constants import PAGE_MARKER_PATTERN
from .section_parser import StyledTextLine

PAGE_MARKER_RE = re.compile(PAGE_MARKER_PATTERN)


def extract_pdf_text(pdf_path: Path | str) -> str:
    return styled_lines_to_text(extract_pdf_lines(pdf_path))


def extract_pdf_lines(pdf_path: Path | str) -> list[StyledTextLine]:
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(path)

    reader = PdfReader(str(path))
    lines: list[StyledTextLine] = []
    for page in reader.pages:
        page_lines = _extract_styled_page_lines(page)
        if page_lines:
            lines.extend(page_lines)
        else:
            lines.extend(StyledTextLine(line) for line in (page.extract_text() or "").splitlines())
    return _normalize_styled_lines(lines)


def styled_lines_to_text(lines: list[StyledTextLine]) -> str:
    return normalize_text("\n".join(line.text for line in lines))


def normalize_text(text: str) -> str:
    """
    Removes whitespaces, etc.
    """
    text = PAGE_MARKER_RE.sub("", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_styled_page_lines(page: Any) -> list[StyledTextLine]:
    builder = _StyledLineBuilder()
    color_stack: list[str | None] = []
    current_color: str | None = None

    def visitor_operand_before(operator: bytes, operands: list[Any], *_args: Any) -> None:
        nonlocal current_color
        op = operator.decode("latin-1") if isinstance(operator, bytes) else str(operator)
        if op == "q":
            color_stack.append(current_color)
        elif op == "Q":
            current_color = color_stack.pop() if color_stack else None
        elif op in {"g", "G"} and operands:
            current_color = _gray_color(operands)
        elif op in {"rg", "RG"} and len(operands) >= 3:
            current_color = _rgb_color(operands)
        elif op in {"k", "K"} and len(operands) >= 4:
            current_color = _cmyk_color(operands)

    def visitor_text(
        text: str,
        _cm: Any,
        _tm: Any,
        font_dict: dict[str, Any] | None,
        font_size: float,
    ) -> None:
        font_name = _font_name(font_dict)
        builder.append(text, font_size, font_name, current_color)

    page.extract_text(
        visitor_operand_before=visitor_operand_before,
        visitor_text=visitor_text,
    )
    return builder.finish()


def _normalize_styled_lines(lines: list[StyledTextLine]) -> list[StyledTextLine]:
    normalized: list[StyledTextLine] = []
    for line in lines:
        text = line.text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"[ \t]+", " ", text).strip()
        if text and not PAGE_MARKER_RE.match(text):
            normalized.append(
                StyledTextLine(
                    text=text,
                    font_size=line.font_size,
                    font_name=line.font_name,
                    color=line.color,
                )
            )
    return normalized


class _StyledLineBuilder:
    def __init__(self) -> None:
        self._parts: list[str] = []
        self._font_sizes: list[float] = []
        self._font_names: list[str] = []
        self._colors: list[str] = []
        self._lines: list[StyledTextLine] = []

    def append(
        self,
        text: str,
        font_size: float | None,
        font_name: str | None,
        color: str | None,
    ) -> None:
        parts = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        for index, part in enumerate(parts):
            if part:
                self._parts.append(part)
                if font_size is not None:
                    self._font_sizes.append(float(font_size))
                if font_name is not None:
                    self._font_names.append(font_name)
                if color is not None:
                    self._colors.append(color)
            if index < len(parts) - 1:
                self._flush()

    def finish(self) -> list[StyledTextLine]:
        self._flush()
        return self._lines

    def _flush(self) -> None:
        text = "".join(self._parts).strip()
        if text:
            self._lines.append(
                StyledTextLine(
                    text=text,
                    font_size=_average(self._font_sizes),
                    font_name=_most_common(self._font_names),
                    color=_most_common(self._colors),
                )
            )
        self._parts = []
        self._font_sizes = []
        self._font_names = []
        self._colors = []


def _font_name(font_dict: dict[str, Any] | None) -> str | None:
    if not font_dict:
        return None
    base_font = font_dict.get("/BaseFont")
    if base_font is None:
        return None
    return str(base_font).lstrip("/")


def _gray_color(operands: list[Any]) -> str:
    value = _pdf_number(operands[0])
    return f"gray:{value:.3f}"


def _rgb_color(operands: list[Any]) -> str:
    values = [_pdf_number(value) for value in operands[:3]]
    return "rgb:" + ",".join(f"{value:.3f}" for value in values)


def _cmyk_color(operands: list[Any]) -> str:
    values = [_pdf_number(value) for value in operands[:4]]
    return "cmyk:" + ",".join(f"{value:.3f}" for value in values)


def _pdf_number(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _average(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def _most_common(values: list[str]) -> str | None:
    if not values:
        return None
    return max(set(values), key=values.count)
