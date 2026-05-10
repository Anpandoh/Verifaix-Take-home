from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel

from ..config import LLMSettings
from .prompts import DEFAULT_SYSTEM_PROMPT

ModelT = TypeVar("ModelT", bound=BaseModel)


class LLMClient:
    def __init__(self, settings: LLMSettings):
        self.settings = settings

    def generate_model(self, prompt: str, model_type: type[ModelT]) -> ModelT:
        from langchain_core.messages import HumanMessage, SystemMessage

        structured_model = self._build_chat_model().with_structured_output(model_type)
        response = structured_model.invoke(
            [
                SystemMessage(content=DEFAULT_SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ]
        )
        if isinstance(response, model_type):
            return response
        return model_type.model_validate(response)

    def _build_chat_model(self) -> Any:
        if self.settings.provider == "none":
            raise RuntimeError(
                "LLM provider is set to 'none'. Configure provider as 'openai' or "
                "'anthropic' before generating artifacts."
            )
        if self.settings.provider == "openai":
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                api_key=self.settings.api_key,
                model=self.settings.model_name,
                temperature=self.settings.temperature,
            )
        if self.settings.provider == "anthropic":
            from langchain_anthropic import ChatAnthropic

            return ChatAnthropic(
                api_key=self.settings.api_key,
                model=self.settings.model_name,
                temperature=self.settings.temperature,
                max_tokens=8192,
            )
        raise ValueError(f"Unsupported LLM provider: {self.settings.provider}")
