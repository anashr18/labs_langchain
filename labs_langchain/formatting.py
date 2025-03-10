from string import Formatter
from typing import Any, Mapping, Sequence, Set, Union


class StrictFormatter(Formatter):
    def check_unused_args(
        self,
        used_args: Set[Union[str, int]],
        args: Sequence,
        kwargs: Mapping[str, Any],
    ) -> None:
        extra = set(kwargs).difference(used_args)
        if extra:
            raise KeyError(f"unused key {extra}")
        # return super().check_unused_args(used_args, args, kwargs)

    def vformat(
        self, format_string: str, args: Sequence, kwargs: Mapping[str, Any]
    ) -> str:
        if len(args) > 0:
            raise ValueError(
                "No positional arguments should be provided, "
                "everything should be passed as keyword arguments."
            )
        return super().vformat(format_string, args, kwargs)


formatter = StrictFormatter()
