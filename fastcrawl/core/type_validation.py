import collections.abc
import dataclasses
import inspect
import types
from typing import Any, Callable, Dict, Iterator, Tuple, Type, Union, get_type_hints


@dataclasses.dataclass
class ReturnType:
    """Represents the return type of a function.

    Attributes:
        func_name (str): The name of the function.
        is_iterator (bool): Whether the return type is an iterator.
        expected_types (Tuple[Type, ...]): A tuple of expected types for the return value.

    """

    func_name: str
    is_iterator: bool
    expected_types: Tuple[Type, ...]


def validate_return_value(return_type: ReturnType, value: Any) -> Iterator[Any]:
    """Validates the return value of a function against its expected return type.

    Args:
        return_type (ReturnType): The expected return type of the function.
        value (Any): The actual return value from the function.

    Raises:
        ValueError: If the return value must be an iterator but is not iterable.
        TypeError: If the return value does not match the expected type.

    Yields:
        Any: The validated return value(s).

    """
    if return_type.is_iterator:
        if not hasattr(value, "__iter__"):
            raise ValueError(
                f"Function `{return_type.func_name}` returned a non-iterable value {value}, "
                f"expected an iterable of {return_type.expected_types}."
            )
        for item in value:
            if not isinstance(item, return_type.expected_types):
                raise TypeError(
                    f"Function `{return_type.func_name}` returned an invalid item {type(item)}, "
                    f"expected iterator of {return_type.expected_types}."
                )
            yield item
    else:
        if not isinstance(value, return_type.expected_types):
            raise TypeError(
                f"Function `{return_type.func_name}` returned an invalid item {type(value)}, "
                f"expected one of {return_type.expected_types}."
            )
        yield value


class TypeValidator:
    """Validator for function type hints.

    Args:
        func (Callable): The function to validate.

    """

    func_name: str
    type_hints: Dict[str, Any]

    def __init__(self, func: Callable) -> None:
        self.func_name = func.__name__
        self.type_hints = get_type_hints(func)

    def validate_required_arg(self, expected_name: str, expected_type: Type) -> Type:
        """Validates that the function has a required argument of the expected type.

        Args:
            expected_name (str): The name of the expected argument.
            expected_type (Type): The expected type of the argument.

        Raises:
            TypeError: If the argument is not found or does not match the expected type.

        Returns:
            Type: The type of the argument if it matches the expected type.

        """
        arg = self.type_hints.get(expected_name)
        if arg is None or not inspect.isclass(arg) or not issubclass(arg, expected_type):
            raise TypeError(
                f"Function `{self.func_name}` must have a `{expected_name}` argument of type {expected_type}."
            )
        return arg

    def validate_return_type(self, expected_types: Tuple[Type, ...], can_be_iterator: bool) -> ReturnType:
        """Validates the return type of the function against expected types.

        Args:
            expected_types (Tuple[Type, ...]): A tuple of expected return types.
            can_be_iterator (bool): Whether the return type can be an iterator.

        Raises:
            TypeError: If the return type does not match the expected types or is invalid.

        Returns:
            ReturnType: Validated return type information.

        """
        return_type = self.type_hints.get("return")

        if return_type is None or return_type is type(None):
            return ReturnType(func_name=self.func_name, is_iterator=False, expected_types=(type(None),))

        is_iterator, return_types = self._is_valid_return_type(return_type, expected_types, can_be_iterator)

        if is_iterator is None or return_types is None:
            error_message = (
                f"Function `{self.func_name}` have an invalid return type hint. "
                f"Expected one of the following or a union of them"
            )
            if can_be_iterator:
                error_message += " or an `Iterator` of them"
            error_message += f": {expected_types}"
            raise TypeError(error_message)

        return ReturnType(func_name=self.func_name, is_iterator=is_iterator, expected_types=return_types)

    def _is_valid_return_type(
        self, return_type: Any, expected_types: Tuple[Type, ...], can_be_iterator: bool = False
    ) -> Tuple[bool | None, Tuple[Type] | None]:
        if self._is_valid_type(return_type, expected_types):
            return False, (return_type,)

        origin_return_type = getattr(return_type, "__origin__", return_type)

        if (origin_return_type is Union or isinstance(origin_return_type, types.UnionType)) and all(
            self._is_valid_type(arg, expected_types) for arg in return_type.__args__
        ):
            return False, tuple(return_type.__args__)

        if can_be_iterator and origin_return_type is collections.abc.Iterator and len(return_type.__args__) == 1:
            return True, self._is_valid_return_type(return_type.__args__[0], expected_types)[1]

        return None, None

    def _is_valid_type(self, actual_type: Any, expected_types: Tuple[Type, ...]) -> bool:
        return inspect.isclass(actual_type) and issubclass(actual_type, expected_types)
