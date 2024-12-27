from typing import Any, AsyncIterator, Optional, Union

import pytest
from httpx import Limits
from pytest_httpx import HTTPXMock

from fastcrawl import (
    BaseCrawler,
    BasePipeline,
    CrawlerHttpClientSettings,
    CrawlerSettings,
    Request,
    Response,
)
from tests.utils import MockStrPipeline


class MockStrDropPipeline(BasePipeline[str]):
    """A mock class for testing the `BasePipeline` class."""

    def __init__(self):
        super().__init__()
        self.counter = 0

    async def process_item(self, item: str) -> Optional[str]:
        """See `BasePipeline` class."""
        self.counter += 1
        if self.counter == 1:
            return item
        return None


class MockCrawler(BaseCrawler):
    """A mock class for testing the `BaseCrawler` class.

    Args:
        first_request_kwargs (Optional[dict[str, Any]]): The keyword arguments to pass
            to the first request. Default is None.
        **kwargs: Additional keyword arguments to pass to the `BaseCrawler` class.

    """

    def __init__(self, first_request_kwargs: Optional[dict[str, Any]] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.first_request_kwargs = first_request_kwargs or {}

    async def generate_requests(self) -> AsyncIterator[Request]:
        """See `BaseCrawler` class."""
        yield Request(url="https://example.com/", callback=self.parse_with_return, **self.first_request_kwargs)

    async def parse_with_return(
        self, response: Response  # pylint: disable=W0613
    ) -> AsyncIterator[Union[Request, str]]:
        """Mock parse method that returns an item and request."""
        yield "test_item_1"
        yield "test_item_2"
        yield Request(url="https://example.com/", callback=self.parse_with_error)

    async def parse_with_error(self, response: Response) -> None:
        """Mock parse method that raises an exception."""
        raise ValueError("Test error")


def test_get_http_client_kwargs() -> None:
    """Tests the `_get_http_client_kwargs` method of the `BaseCrawler` class."""
    query_params = {"param": "value"}
    limits = Limits(max_connections=10, max_keepalive_connections=5, keepalive_expiry=60)

    crawler = MockCrawler(
        settings=CrawlerSettings(
            http_client=CrawlerHttpClientSettings(
                query_params=query_params,
                max_connections=limits.max_connections,
                max_keepalive_connections=limits.max_keepalive_connections,
                keepalive_expiry=limits.keepalive_expiry,
            )
        )
    )

    kwargs = crawler._get_http_client_kwargs()  # pylint: disable=W0212
    assert kwargs["params"] == query_params
    assert kwargs["limits"] == limits


@pytest.mark.asyncio
async def test_run(httpx_mock: HTTPXMock) -> None:
    """Tests the `run` method of the `BaseCrawler` class."""
    httpx_mock.add_response()
    httpx_mock.add_response()

    crawler = MockCrawler(
        settings=CrawlerSettings(
            pipelines=[MockStrPipeline(), MockStrDropPipeline()],
        ),
        first_request_kwargs={
            "query_params": {"key": "value"},
            "form_data": {"key": "value"},
            "json_data": {"key": "value"},
        },
    )
    await crawler.run()
