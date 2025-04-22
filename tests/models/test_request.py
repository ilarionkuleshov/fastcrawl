import pytest
from httpx import URL

from tests.mocks import create_request


@pytest.mark.parametrize(
    ["method", "url", "convert_to_httpx_url"],
    [
        ("GET", "https://example.com/1", False),
        ("POST", "https://example.com/2", False),
        ("PUT", "https://example.com/3", True),
        ("DELETE", "https://example.com/4", True),
    ],
)
def test_str(method: str, url: str, convert_to_httpx_url: bool) -> None:
    """Tests the `__str__` method of the `Request` class.

    Args:
        method (str): Method for the request.
        url (str): URL for the request.
        convert_to_httpx_url (bool): Whether to convert the URL to an `httpx.URL` object.

    """
    request = create_request(method=method, url=URL(url) if convert_to_httpx_url else url)
    assert str(request) == f"<Request({method}, {url})>"
