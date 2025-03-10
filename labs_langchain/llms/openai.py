import os
from typing import Any, Dict, List, Mapping, Optional

from openai import OpenAI as OpenAIClient
from pydantic import BaseModel, ConfigDict, model_validator

from labs_langchain.llms.base import LLM


class OpenAI(BaseModel, LLM):
    client: Any
    model_name: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 256
    top_p: int = 1
    frequency_penalty: int = 0
    presence_penalty: int = 0
    n: int = 1

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("Missing OPENAI_API_KEY")
        values["client"] = OpenAIClient(api_key=api_key)
        return values

    @property
    def default_params(self) -> Mapping[str, Any]:
        return {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "n": self.n,
        }

    def __call__(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            stop=stop,
            **self.default_params,
        )
        # print(f"response::{response}")
        return response.choices[0].message.content
