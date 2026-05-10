from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> str:
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")
    return sha256_text(content)


def dumps_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, default=str)
