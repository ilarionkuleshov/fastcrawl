from datetime import timedelta
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Sequence,
    Union,
)

from httpx import URL
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from fastcrawl.models.response import Response

PrimitiveData = str | int | float | bool | None
RequestCallback = Callable[["Response"], Awaitable[AsyncIterator[Union[BaseModel, "Request"]]]]


class Request(BaseModel):
    """Request model.

    Attributes:
        method (str): HTTP method. Default is "GET".
        url (URL | str): URL to request.
        callback (RequestCallback): Callback to handle the response.
        query_params (dict[str, PrimitiveData, Sequence[PrimitiveData]] | None): Query parameters
            for the URL. Default is None.
        headers (dict[str, str] | None): Headers for the request. Default is None.
        cookies (dict[str, str] | None): Cookies for the request. Default is None.
        form_data (dict[str, Any] | None): Form data for the request. Default is None.
        json_data (Any | None): JSON data for the request. Default is None.
        files (dict[str, bytes] | None): Files for the request. Default is None.
        auth (tuple[str, str] | None): Authentication credentials. Default is None.
        timeout (timedelta | None): Timeout for the request. Default is None.
        follow_redirects (bool | None): Whether to follow redirects. Default is True.

    """

    method: str = "GET"
    url: URL | str
    callback: RequestCallback
    query_params: dict[str, PrimitiveData | Sequence[PrimitiveData]] | None = None
    headers: dict[str, str] | None = None
    cookies: dict[str, str] | None = None
    form_data: dict[str, Any] | None = None
    json_data: Any | None = None
    files: dict[str, bytes] | None = None
    auth: tuple[str, str] | None = None
    timeout: timedelta | None = None
    follow_redirects: bool | None = True

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.method}, {self.url})>"
