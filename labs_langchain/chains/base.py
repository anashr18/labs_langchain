"""Base interface for all chains"""

import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Chain(ABC):

    @property
    @abstractmethod
    def input_keys(self) -> List[str]:
        """Input keys that chain expects"""

    @property
    @abstractmethod
    def output_keys(self) -> List[str]:
        """Output keys that chain expects"""

    def _validate_inputs(self, inputs: Dict[str, str]) -> None:
        """Validate inputs"""
        missing_keys = set(self.input_keys).difference(inputs)
        if missing_keys:
            class_name = self.__class__.__name__  # Get the class name
            method_name = sys._getframe().f_code.co_name  # Get the method name
            raise ValueError(
                f"{class_name}.{method_name}: Missing some input keys {missing_keys}"
            )

    def _validate_outputs(self, outputs: Dict[str, str]) -> None:
        """Validate outputs"""
        # print(f"outputs::{outputs}")
        # print(f"output_keys::{self.output_keys}")
        if set(self.output_keys) != set(outputs):
            class_name = self.__class__.__name__  # Get the class name
            method_name = sys._getframe().f_code.co_name  # Get the method name
            raise ValueError(
                f"{class_name}.{method_name}:"
                f"Did not get output keys as expected\n"
                f"Got: {set(outputs)} expected: {set(self.output_keys)}."
            )

    @abstractmethod
    def _run(self, inputs: Dict[str, str]) -> Dict[str, str]:
        """run the chain"""

    def __call__(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        self._validate_inputs(inputs)
        outputs = self._run(inputs)
        self._validate_outputs(outputs)
        return {**inputs, **outputs}
