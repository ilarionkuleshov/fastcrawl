from typing import Any, Callable, Iterator

from fastcrawl.core import type_validation


class Component:

    func: Callable
    return_type: type_validation.ReturnType

    def __init__(self, func: Callable, return_type: type_validation.ReturnType) -> None:
        self.func = func
        self.return_type = return_type

    def run_iter(self, **kwargs) -> Iterator[Any]:
        result = self.func(**kwargs)
        yield from type_validation.validate_return_value(self.return_type, result)

    def run(self, **kwargs) -> Any:
        return next(self.run_iter(**kwargs))
