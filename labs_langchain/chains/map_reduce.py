"""Map-reduce chain wrapper."""
from typing import Dict, List
from pydantic import BaseModel
from labs_langchain.chains.base import Chain
from labs_langchain.chains.llm import LLMChain
from labs_langchain.llms.base import LLM
from labs_langchain.prompt import Prompt
from labs_langchain.text_splitter import TextSplitter

class MapReduceChain(Chain, BaseModel):
    map_llm: LLMChain
    reduce_llm: LLMChain
    text_splitter: TextSplitter
    input_key:str = "input_text"
    output_key:str = "output"

    model_config = {"extra": "forbid", "arbitrary_types_allowed": True}

    @classmethod
    def from_params(cls, llm:LLM, prompt: Prompt, text_splitter: TextSplitter)-> "MapReduceChain":
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        return cls(map_llm=llm_chain, reduce_llm=llm_chain, text_splitter=text_splitter)

    @property
    def input_keys(self) -> List[str]:
        """Input keys that the chain expects."""
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        """Output keys that the chain expects."""
        return [self.output_key]

    def _run(self, inputs: Dict[str, str]) -> Dict[str, str]:
        """Run the chain."""
        text_input: List[str] = self.text_splitter.split_text(inputs[self.input_key])
        summaries: List[str] = []
        for d in text_input:
            input_param = {self.map_llm.prompt.input_variables[0]:d}
            summary = self.map_llm.predict(**input_param)
            summaries.append(summary)
        reduce_input = "\n".join(summaries)
        reduce_param = {self.reduce_llm.prompt.input_variables[0]: reduce_input}
        final_text = self.reduce_llm.predict(**reduce_param)
        return {self.output_key: final_text}
    
    def run(self, input: str):
        """Friendly interface for chain."""
        return self({self.input_key: input})[self.output_key]
            