from typing import Any, Dict, List

from pydantic import BaseModel, model_validator

from labs_langchain.formatting import formatter

_FORMATTER_MAPPING = {"f-string": formatter.format}


class Prompt(BaseModel):
    input_variables: List[str]
    template: str
    template_format: str = "f-string"

    model_config = {"extra": "forbid"}

    def format(self, **kwargs: Any) -> str:
        return _FORMATTER_MAPPING[self.template_format](self.template, **kwargs)

    @model_validator(mode="before")
    @classmethod
    def validate_template(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        input_variables = values["input_variables"]
        template = values["template"]
        # template_format = values["template_format"]
        template_format = values.get("template_format", "f-string")
        if template_format not in _FORMATTER_MAPPING:
            valid_formats = list(_FORMATTER_MAPPING)
            raise ValueError(
                f"invalid template format. Got `{template_format}`;"
                f"should be one of them {valid_formats}"
            )
        dummy_inputs = {input_var: "foo" for input_var in input_variables}
        try:
            formatter_func = _FORMATTER_MAPPING[template_format]
            formatter_func(template, **dummy_inputs)
        except KeyError:
            raise ValueError("Invalid prompt schema")
        return values
