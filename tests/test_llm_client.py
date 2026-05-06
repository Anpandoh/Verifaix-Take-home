from pydantic import BaseModel

from swgen_test_automation.config import LLMSettings
from swgen_test_automation.llm_client import LLMClient


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
    assert "Create output" in fake_chat.structured_model.messages[-1].content


def test_generate_model_validates_dict_responses_from_langchain(monkeypatch) -> None:
    fake_chat = FakeChatModel({"value": "ok"})
    monkeypatch.setattr(LLMClient, "_build_chat_model", lambda _self: fake_chat)

    result = LLMClient(_settings()).generate_model("Create output", SampleOutput)

    assert result == SampleOutput(value="ok")
