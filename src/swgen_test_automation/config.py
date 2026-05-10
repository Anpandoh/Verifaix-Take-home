from __future__ import annotations

import os
import tomllib
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field, model_validator

from .constants import (
    DEFAULT_CONFIG_PATH,
    DEFAULT_DATABASE_PATH,
    DEFAULT_GENERATED_DIR,
    DEFAULT_REPORTS_DIR,
    DOTENV_PATH,
    EXAMPLE_CONFIG_PATH,
)


class AppSettings(BaseModel):
    database_path: Path = DEFAULT_DATABASE_PATH
    generated_dir: Path = DEFAULT_GENERATED_DIR
    reports_dir: Path = DEFAULT_REPORTS_DIR


class LLMSettings(BaseModel):
    provider: str = Field(default="none", pattern="^(openai|anthropic|none)$")
    model_name: str = ""
    api_key_env: str = ""
    temperature: float = 0.1
    use_llm_for_testplan: bool = True
    use_llm_for_code: bool = True
    use_llm_for_tests: bool = True

    @model_validator(mode="after")
    def require_provider_settings(self) -> "LLMSettings":
        if self.provider == "none":
            return self
        if not self.model_name:
            raise ValueError("model_name is required when llm.provider is not 'none'.")
        if not self.api_key_env:
            raise ValueError("api_key_env is required when llm.provider is not 'none'.")
        return self

    @property
    def api_key(self) -> str:
        if self.provider == "none":
            raise RuntimeError("No API key is available because llm.provider is set to 'none'.")
        value = os.getenv(self.api_key_env)
        if not value:
            raise RuntimeError(
                f"Missing API key. Set environment variable {self.api_key_env!r}."
            )
        return value


class Settings(BaseModel):
    app: AppSettings = AppSettings()
    llm: LLMSettings = LLMSettings()


def load_settings(config_path: Path | str = DEFAULT_CONFIG_PATH) -> Settings:
    load_dotenv(DOTENV_PATH, override=False)
    path = Path(config_path)
    load_dotenv(path.parent / DOTENV_PATH, override=False)
    if not path.exists():
        if EXAMPLE_CONFIG_PATH.exists():
            path = EXAMPLE_CONFIG_PATH
        else:
            return Settings()

    with path.open("rb") as f:
        raw = tomllib.load(f)
    return Settings.model_validate(raw)
