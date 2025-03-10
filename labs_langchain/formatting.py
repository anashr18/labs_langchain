"""Utilities for formatting class."""

from string import Formatter
from typing import Any, Mapping, Sequence, Set, Union


class StrictFormatter(Formatter):
    """Subclass of Formatter with strict argument checking."""

    def check_unused_args(
        self,
        used_args: Set[Union[str, int]],
        args: Sequence,
        kwargs: Mapping[str, Any],
    ) -> None:
        """Override Formatter class method to check unused key arguments."""
        extra = set(kwargs).difference(used_args)
        if extra:
            raise KeyError(f"unused key {extra}")
        # return super().check_unused_args(used_args, args, kwargs)

    def vformat(
        self, format_string: str, args: Sequence, kwargs: Mapping[str, Any]
    ) -> str:
        """Raise error in case of positional arguments are provided."""
        if len(args) > 0:
            raise ValueError(
                "No positional arguments should be provided, "
                "everything should be passed as keyword arguments."
            )
        return super().vformat(format_string, args, kwargs)


formatter = StrictFormatter()
