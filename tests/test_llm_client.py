import pytest
from pydantic import BaseModel

from module_generator.config import LLMSettings
from module_generator.llm import LLMClient
from module_generator.llm.prompts import DEFAULT_SYSTEM_PROMPT


class SampleOutput(BaseModel):
    value: str


class FakeStructuredModel:
    def __init__(self, response):
        self.response = response
        self.messages = None

    def invoke(self, messages):
        self.messages = messages
        return self.response


class FakeChatModel:
    def __init__(self, response):
        self.response = response
        self.structured_model = None
        self.model_type = None

    def with_structured_output(self, model_type):
        self.model_type = model_type
        self.structured_model = FakeStructuredModel(self.response)
        return self.structured_model


def _settings() -> LLMSettings:
    return LLMSettings(provider="openai", model_name="fake-model", api_key_env="FAKE_API_KEY")


def test_generate_model_uses_langchain_structured_output(monkeypatch) -> None:
    fake_chat = FakeChatModel(SampleOutput(value="ok"))
    monkeypatch.setattr(LLMClient, "_build_chat_model", lambda _self: fake_chat)

    result = LLMClient(_settings()).generate_model("Create output", SampleOutput)

    assert result == SampleOutput(value="ok")
    assert fake_chat.model_type is SampleOutput
    assert fake_chat.structured_model.messages[0].content == DEFAULT_SYSTEM_PROMPT
    assert "Create output" in fake_chat.structured_model.messages[-1].content


def test_generate_model_validates_dict_responses_from_langchain(monkeypatch) -> None:
    fake_chat = FakeChatModel({"value": "ok"})
    monkeypatch.setattr(LLMClient, "_build_chat_model", lambda _self: fake_chat)

    result = LLMClient(_settings()).generate_model("Create output", SampleOutput)

    assert result == SampleOutput(value="ok")


def test_none_provider_fails_before_building_chat_model() -> None:
    settings = LLMSettings(provider="none")

    with pytest.raises(RuntimeError, match="provider is set to 'none'"):
        LLMClient(settings)._build_chat_model()
