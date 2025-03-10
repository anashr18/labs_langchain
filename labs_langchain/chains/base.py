"""Base interface for all chains."""

import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Chain(ABC):
    """Base class for all chains."""

    @property
    @abstractmethod
    def input_keys(self) -> List[str]:
        """Input keys that the chain expects."""

    @property
    @abstractmethod
    def output_keys(self) -> List[str]:
        """Output keys that the chain expects."""

    def _validate_inputs(self, inputs: Dict[str, str]) -> None:
        """Validate inputs.

        Potentially raise an error if missing input keys.
        """
        missing_keys = set(self.input_keys).difference(inputs)
        if missing_keys:
            class_name = self.__class__.__name__  # Get the class name
            method_name = sys._getframe().f_code.co_name  # Get the method name
            raise ValueError(
                f"{class_name}.{method_name}: Missing some input keys {missing_keys}"
            )

    def _validate_outputs(self, outputs: Dict[str, str]) -> None:
        """Validate outputs.

        Raise an error if the output keys do not match exactly the expected output keys.
        """
        if set(self.output_keys) != set(outputs):
            class_name = self.__class__.__name__  # Get the class name
            method_name = sys._getframe().f_code.co_name  # Get the method name
            raise ValueError(
                f"{class_name}.{method_name}: "
                f"Did not get output keys as expected\n"
                f"Got: {set(outputs)} expected: {set(self.output_keys)}."
            )

    @abstractmethod
    def _run(self, inputs: Dict[str, str]) -> Dict[str, str]:
        """Run the chain."""

    def __call__(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate inputs, run the chain, and validate outputs."""
        self._validate_inputs(inputs)
        outputs = self._run(inputs)
        self._validate_outputs(outputs)
        return {**inputs, **outputs}
