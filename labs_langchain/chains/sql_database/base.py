"""Sql wrapper chain."""

from typing import Any, Dict, List

from pydantic import BaseModel

from labs_langchain.chains.base import Chain
from labs_langchain.chains.llm import LLMChain
from labs_langchain.chains.sql_database.prompt import PROMPT
from labs_langchain.llms.base import LLM
from labs_langchain.sql_database import SqlDatabase


class SqlDatabaseChain(Chain, BaseModel):
    """Sql wrapper chain"""

    llm: LLM
    database: SqlDatabase
    input_key: str = "query"
    output_key: str = "result"

    model_config = {"extra": "forbid", "arbitrary_types_allowed": True}

    @property
    def input_keys(self) -> List[str]:
        """Return the input keys"""
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        """Return the input keys"""
        return [self.output_key]

    def _run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        llm_chain = LLMChain(llm=self.llm, prompt=PROMPT)
        _input = inputs[self.input_key] + "\nSQLQuery: "
        llm_inputs = {
            "dialect": self.database.dialect,
            "table_info": self.database.table_info,
            "input": _input,
        }
        sql_cmd = llm_chain.predict(**llm_inputs)
        print(sql_cmd)
        result = self.database.run(sql_cmd)
        print(result)
        _input += f"\nSQLResult: {result}\nAnswer: "
        llm_inputs["input"] = _input
        final_answer = llm_chain.predict(**llm_inputs)
        return {self.output_key: final_answer}

    def query(self, query: str) -> str:
        """Run natural language query against a SQL database."""
        return self({self.input_key: query})[self.output_key]
