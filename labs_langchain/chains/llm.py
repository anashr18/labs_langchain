"""LLMChain class for running prompt-based language model chains."""

from typing import Any, Dict, List

from pydantic import BaseModel

from labs_langchain.chains.base import Chain
from labs_langchain.llms.base import LLM
from labs_langchain.prompt import Prompt


class LLMChain(Chain, BaseModel):
    """A chain that runs a prompt-based language model."""

    prompt: Prompt
    llm: LLM
    output_key: str = "text"

    model_config = {"extra": "forbid", "arbitrary_types_allowed": True}

    @property
    def input_keys(self) -> List[str]:
        """Return the expected input keys for the prompt."""
        return self.prompt.input_variables

    @property
    def output_keys(self) -> List[str]:
        """Return the expected output keys."""
        return [self.output_key]

    def _run(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Run the chain by formatting the prompt and passing it to the LLM.

        Args:
            inputs (Dict[str, Any]): The input dictionary containing values
            for the prompt.

        Returns:
            Dict[str, str]: A dictionary containing the generated output text.
        """
        selected_inputs = {k: inputs[k] for k in self.prompt.input_variables}
        actual_prompt = self.prompt.format(**selected_inputs)

        kwargs = {}
        if "stop" in inputs:
            kwargs["stop"] = inputs["stop"]

        response = self.llm(actual_prompt, **kwargs)
        return {self.output_key: response}

    def predict(self, **kwargs: Any) -> str:
        """Predict the output based on the provided keyword arguments.

        Returns:
            str: The generated text output.
        """
        return self(kwargs)[self.output_key]
