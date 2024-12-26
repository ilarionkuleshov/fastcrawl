from typing import Callable

from httpx import URL
from httpx import Request as HttpxRequest
from httpx import Response as HttpxResponse

from fastcrawl import BasePipeline, Request, Response


class MockStrPipeline(BasePipeline[str]):
    """A mock class for testing the `BasePipeline` class."""

    async def process_item(self, item: str) -> str | None:
        """See `BasePipeline` class."""
        return item * 2


def create_request(url: URL | str = "https://example.com/", callback: Callable = lambda _: None, **kwargs) -> Request:
    """Returns request instance.

    Args:
        url (URL | str): URL for the request. Default is "https://example.com/".
        callback (Callable): Callback for the request. Default is lambda _: None.
        **kwargs: Additional keyword arguments.

    """
    return Request(url=url, callback=callback, **kwargs)


def create_response(
    url: URL = URL("https://example.com/"),
    status_code: int = 200,
    content: bytes = b"",
    text: str = "",
    request: Request | None = None,
    **kwargs,
) -> Response:
    """Returns response instance.

    Args:
        url (URL): URL for the response. Default is URL("https://example.com/").
        status_code (int): Status code for the response. Default is 200.
        content (bytes): Content for the response. Default is b"".
        text (str): Text for the response. Default is "".
        request (Request | None): Request instance for the response.
            If not provided, a new request instance will be created. Default is None.
        **kwargs: Additional keyword arguments.

    """
    if request is None:
        request = create_request()
    return Response(
        url=url,
        status_code=status_code,
        content=content,
        text=text,
        request=request,
        **kwargs,
    )


def create_httpx_request(method: str = "GET", url: URL | str = "https://example.com/", **kwargs) -> HttpxRequest:
    """Returns httpx request instance.

    Args:
        method (str): HTTP method for the request. Default is "GET".
        url (URL | str): URL for the request. Default is "https://example.com/".
        **kwargs: Additional keyword arguments.

    """
    return HttpxRequest(method=method, url=url, **kwargs)


def create_httpx_response(status_code: int = 200, httpx_request: HttpxRequest | None = None, **kwargs) -> HttpxResponse:
    """Returns httpx response instance.

    Args:
        status_code (int): Status code for the response. Default is 200.
        httpx_request (HttpxRequest | None): Httpx request instance for the response.
            If not provided, a new httpx request instance will be created. Default is None.
        **kwargs: Additional keyword arguments.

    """
    if httpx_request is None:
        httpx_request = create_httpx_request()
    return HttpxResponse(
        status_code=status_code,
        request=httpx_request,
        **kwargs,
    )
