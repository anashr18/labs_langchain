"""Base interface for LLM"""
from abc import ABC, abstractmethod
from typing import Optional, List
class LLM(ABC):
    """LLM wrapper should take in a prompt"""
    @abstractmethod
    def __call__(self, prompt: str, stop: Optional[List[str]])->str:
        """Run the LLM on given prompt"""