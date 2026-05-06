from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader


PAGE_MARKER_RE = re.compile(r"--\s*\d+\s+of\s+\d+\s*--")


def extract_pdf_text(pdf_path: Path | str) -> str:
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(path)

    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return normalize_text("\n".join(pages))


def normalize_text(text: str) -> str:
    text = PAGE_MARKER_RE.sub("", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
