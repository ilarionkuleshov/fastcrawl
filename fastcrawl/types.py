from typing import TYPE_CHECKING, Any, AsyncIterator, Callable, Coroutine

if TYPE_CHECKING:
    from fastcrawl.models import Response

PrimitiveData = str | int | float | bool | None

RequestCallback = Callable[["Response"], Coroutine[Any, Any, AsyncIterator[Any] | None] | AsyncIterator[Any]]
QueryParams = dict[str, PrimitiveData | list[PrimitiveData]]
Headers = dict[str, str]
Cookies = dict[str, str]
FormData = dict[str, Any]
JsonData = Any
Files = dict[str, bytes]
Auth = tuple[str, str]
