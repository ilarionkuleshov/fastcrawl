from httpx import URL
from httpx import Request as HttpxRequest
from httpx import Response as HttpxResponse

from fastcrawl.models import Request, Response


def create_request(**kwargs) -> Request:
    """Returns a request instance with default values."""
    kwargs["url"] = kwargs.get("url", "https://example.com/")
    kwargs["callback"] = kwargs.get("callback", lambda _: None)
    return Request(**kwargs)


def create_response(**kwargs) -> Response:
    """Returns a response instance with default values."""
    kwargs["url"] = kwargs.get("url", URL("https://example.com/"))
    kwargs["status_code"] = kwargs.get("status_code", 200)
    kwargs["content"] = kwargs.get("content", b"")
    kwargs["text"] = kwargs.get("text", "")
    kwargs["request"] = kwargs.get("request", create_request())
    return Response(**kwargs)


def create_httpx_response(**kwargs) -> HttpxResponse:
    """Returns an httpx response instance with default values."""
    kwargs["status_code"] = kwargs.get("status_code", 200)
    kwargs["request"] = kwargs.get("request", HttpxRequest("GET", "https://example.com/"))
    return HttpxResponse(**kwargs)
