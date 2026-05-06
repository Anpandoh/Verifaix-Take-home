from __future__ import annotations

import os
import tomllib
from pathlib import Path

from pydantic import BaseModel, Field


class AppSettings(BaseModel):
    database_path: Path = Path("data/swgen.sqlite")
    generated_dir: Path = Path("generated")
    reports_dir: Path = Path("reports")


class LLMSettings(BaseModel):
    provider: str = Field(default="openai", pattern="^(openai|anthropic)$")
    model_name: str
    api_key_env: str
    temperature: float = 0.1
    use_llm_for_testplan: bool = True
    use_llm_for_code: bool = True
    use_llm_for_tests: bool = True

    @property
    def api_key(self) -> str:
        value = os.getenv(self.api_key_env)
        if not value:
            raise RuntimeError(
                f"Missing API key. Set environment variable {self.api_key_env!r}."
            )
        return value


class Settings(BaseModel):
    app: AppSettings = AppSettings()
    llm: LLMSettings = LLMSettings(
        provider="openai",
        model_name="gpt-4.1-mini",
        api_key_env="OPENAI_API_KEY",
    )


def load_settings(config_path: Path | str = "config.toml") -> Settings:
    path = Path(config_path)
    if not path.exists():
        example = Path("config.example.toml")
        if example.exists():
            path = example
        else:
            return Settings()

    with path.open("rb") as f:
        raw = tomllib.load(f)
    return Settings.model_validate(raw)
