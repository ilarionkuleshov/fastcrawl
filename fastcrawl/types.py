from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Callable,
    Coroutine,
    Mapping,
    Sequence,
)

if TYPE_CHECKING:
    from fastcrawl.models import Response  # pragma: no cover

PrimitiveData = str | int | float | bool | None

RequestCallback = Callable[["Response"], Coroutine[Any, Any, AsyncIterator[Any] | None] | AsyncIterator[Any]]
QueryParams = Mapping[str, PrimitiveData | Sequence[PrimitiveData]]
Headers = Mapping[str, str]
Cookies = Mapping[str, str]
FormData = Mapping[str, Any]
JsonData = Any
Files = Mapping[str, bytes]
Auth = tuple[str, str]
