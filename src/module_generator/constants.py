from __future__ import annotations

from pathlib import Path

DEFAULT_CONFIG_PATH = Path("config.toml")
EXAMPLE_CONFIG_PATH = Path("config.example.toml")
DOTENV_PATH = Path(".env")

DEFAULT_DATABASE_PATH = Path("data/swgen.sqlite")
DEFAULT_GENERATED_DIR = Path("generated")
DEFAULT_REPORTS_DIR = DEFAULT_GENERATED_DIR / "reports"

DEFAULT_SAMPLE_PDF = "/Users/anpandoh/Downloads/Problem_Description_Software_Coding.pdf"

PAGE_MARKER_PATTERN = r"--\s*\d+\s+of\s+\d+\s*--"
TEST_PLAN_ID_PATTERN = r"TP_\d+(?:\.\d+)?"
