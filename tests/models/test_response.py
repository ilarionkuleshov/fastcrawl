import json
from typing import AsyncIterator

import pytest
from httpx import URL
from parsel import Selector

from fastcrawl import Response
from tests.mocks import create_httpx_response, create_request, create_response


async def mock_iter_content(chunks: list[bytes]) -> AsyncIterator[bytes]:
    """Yields chunks of bytes.

    Args:
        chunks (list[bytes]): List of bytes chunks.

    """
    for chunk in chunks:
        yield chunk


@pytest.mark.asyncio
async def test_from_httpx_response_with_iter_content() -> None:
    """Tests the `from_httpx_response` method with an async iterator content."""
    chunks = [b"Hello, ", b"world!"]
    httpx_response = create_httpx_response(content=mock_iter_content(chunks))

    response = await Response.from_httpx_response(
        httpx_response, create_request()
    )
    assert response.content == b"Hello, world!"
    assert response.text == "Hello, world!"


def test_get_json_data_with_valid_json() -> None:
    """Tests the `get_json_data` method with valid JSON."""
    json_data = {"key": "value"}
    response = create_response(text=json.dumps(json_data))
    assert response.get_json_data() == json_data


def test_get_json_data_with_invalid_json() -> None:
    """Tests the `get_json_data` method with invalid JSON."""
    response = create_response(text="invalid")
    with pytest.raises(json.JSONDecodeError):
        response.get_json_data()


@pytest.mark.parametrize("text", ["", "<html></html>", "<xml></xml>"])
def test_selector(text: str) -> None:
    """Tests the `selector` property of the `Response` class.

    Args:
        text (str): Text content for the response.

    """
    response = create_response(text=text)
    selector = response.selector

    expected_selector = Selector(text=text)

    assert selector._text == expected_selector._text  # pylint: disable=W0212
    assert selector.type == expected_selector.type


@pytest.mark.parametrize(
    ["status_code", "url"],
    [
        (200, "https://example.com/1"),
        (404, "https://example.com/2"),
    ],
)
def test_str(status_code: int, url: str) -> None:
    """Tests the `__str__` method of the `Response` class.

    Args:
        status_code (int): Status code for the response.
        url (str): URL for the response.

    """
    response = create_response(status_code=status_code, url=URL(url))
    assert str(response) == f"<Response({status_code}, {url})>"
