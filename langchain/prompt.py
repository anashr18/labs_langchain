from pydantic import BaseModel
from typing import List, Any
from langchain.formatting import formatter 

_FORMATTER_MAPPING = {
    "f-string": formatter.format
}
class Prompt(BaseModel):
    input_variables: List[str]
    template: str
    template_format: str =  "f-string"

    model_config = {
        "extra": "forbid"
    }

    def format(self, **kwargs):
        return _FORMATTER_MAPPING[self.template_format](self.template, **kwargs)


    