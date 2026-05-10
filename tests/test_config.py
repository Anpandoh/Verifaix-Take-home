from pathlib import Path

from swgen_test_automation.config import load_settings


def test_missing_config_defaults_to_no_llm_provider(tmp_path: Path) -> None:
    settings = load_settings(tmp_path / "missing.toml")

    assert settings.llm.provider == "none"
    assert settings.llm.model_name == ""
    assert settings.llm.api_key_env == ""


def test_load_settings_reads_api_key_from_dotenv(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text("TEST_PROVIDER_KEY=secret-from-dotenv\n", encoding="utf-8")
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        """
[llm]
provider = "anthropic"
model_name = "fake-model"
api_key_env = "TEST_PROVIDER_KEY"
temperature = 0.1
""",
        encoding="utf-8",
    )

    settings = load_settings(config_path)

    assert settings.llm.api_key == "secret-from-dotenv"


def test_load_settings_accepts_none_provider_without_model_or_api_key(tmp_path: Path) -> None:
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        """
[llm]
provider = "none"
use_llm_for_testplan = false
use_llm_for_code = false
use_llm_for_tests = false
""",
        encoding="utf-8",
    )

    settings = load_settings(config_path)

    assert settings.llm.provider == "none"
    assert settings.llm.model_name == ""
    assert settings.llm.api_key_env == ""
