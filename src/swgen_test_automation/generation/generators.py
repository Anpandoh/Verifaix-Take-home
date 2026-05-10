from __future__ import annotations

from ..llm import LLMClient
from ..schemas import GeneratedModule, GeneratedTestSuite, Section, TestPlan
from ..utils import dumps_json
from .prompts import CODE_PROMPT, TEST_PLAN_PROMPT, TESTS_PROMPT


def render_sections(sections: list[Section]) -> str:
    return "\n\n".join(
        f"Section {section.id}: {section.title}\n{section.text}" for section in sections
    )


class Generators:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def create_test_plan(
        self,
        version: str,
        description_version: str,
        sections: list[Section],
    ) -> tuple[TestPlan, str]:
        prompt = TEST_PLAN_PROMPT.format(
            version=version,
            description_version=description_version,
            sections=render_sections(sections),
        )
        return self.llm.generate_model(prompt, TestPlan), prompt

    def create_module(
        self,
        version: str,
        sections: list[Section],
        test_plan: TestPlan,
    ) -> tuple[GeneratedModule, str]:
        prompt = CODE_PROMPT.format(
            version=version,
            sections=render_sections(sections),
            test_plan=dumps_json(test_plan.model_dump()),
        )
        return self.llm.generate_model(prompt, GeneratedModule), prompt

    def create_tests(
        self,
        version: str,
        sections: list[Section],
        test_plan: TestPlan,
        generated_module: GeneratedModule,
    ) -> tuple[GeneratedTestSuite, str]:
        prompt = TESTS_PROMPT.format(
            version=version,
            sections=render_sections(sections),
            test_plan=dumps_json(test_plan.model_dump()),
            generated_module=dumps_json(generated_module.model_dump()),
        )
        return self.llm.generate_model(prompt, GeneratedTestSuite), prompt
