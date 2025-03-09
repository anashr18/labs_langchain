import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pydantic import BaseModel
from langchain.chains.base import Chain
from langchain.prompt import Prompt
from langchain.llms.base import LLM
from typing import List, Dict, Any

class LLMChain(Chain, BaseModel):
    prompt: Prompt
    llm: LLM
    output_key: str="text"

    model_config = {
        "extra": "forbid",
        "arbitrary_types_allowed": True
    }
    @property
    def input_keys(self)->List[str]:
        return self.prompt.input_variables
    
    @property
    def output_keys(self) -> List[str]:
        return [self.output_key]
    
    def _run(self, inputs: Dict[str, str])-> Dict[str, str]:
        # print(inputs)
        selected_inputs = {k:inputs[k] for k in self.prompt.input_variables}
        # print(f"selected_inputs:: {selected_inputs}")
        actual_prompt = self.prompt.format(**selected_inputs)
        # print(f"actual_prompt:: {actual_prompt}")
        
        kwargs = {}
        if "stop" in inputs:
            kwargs["stop"] = inputs["stop"]
        response = self.llm(actual_prompt, **kwargs)
        return {self.output_key: response}


    def predict(self, **kwargs: Any)-> str:
        return self(kwargs)[self.output_key]
