from typing import Any, Callable, Iterator, Type

from fastcrawl.core import type_validation


class Component:
    """Wrapper for components like handlers or pipelines.

    Args:
        func (Callable): The function to be wrapped.
        arg_type (Type): The expected type of the function's main argument.
        return_type (type_validation.ReturnType): The expected return type of the function.

    """

    func: Callable
    return_type: type_validation.ReturnType

    def __init__(self, func: Callable, arg_type: Type, return_type: type_validation.ReturnType) -> None:
        self.func = func
        self.arg_type = arg_type
        self.return_type = return_type

    def is_valid_arg(self, arg: Any) -> bool:
        """Returns True if the argument is of the expected type, False otherwise."""
        return isinstance(arg, self.arg_type)

    def run_iter(self, **kwargs) -> Iterator[Any]:
        """Yields the result of the function call, validating its return type."""
        result = self.func(**kwargs)
        yield from type_validation.validate_return_value(self.return_type, result)

    def run(self, **kwargs) -> Any:
        """Returns the result of the function call, validating its return type."""
        return next(self.run_iter(**kwargs))
