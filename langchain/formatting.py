from string import Formatter
from typing import Sequence, Mapping, Any, Union

class StrictFormatter(Formatter):
    def check_unused_args(self, used_args: Sequence[Union[str, int]], args: Sequence, kwargs:Mapping[str, Any]):
        extra = set(used_args).difference(kwargs)
        if extra:
            raise KeyError(f"unused key {extra}")
        return super().check_unused_args(used_args, args, kwargs)

    def vformat(self, format_string: str, args: Sequence, kwargs: Mapping[str, Any])-> str:
        if len(args) > 0:
            raise ValueError(
                "No positional arguments should be provided, "
                "everything should be passed as keyword arguments."
            )
        return super().vformat(format_string, args, kwargs)

formatter = StrictFormatter()