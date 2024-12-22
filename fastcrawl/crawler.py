import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, AsyncIterator

from httpx import AsyncClient, Timeout

from fastcrawl.models import CrawlerConfig, Request, Response


class Crawler(ABC):
    """Base for all crawlers.

    Attributes:
        logger (logging.Logger): Logger for the crawler.
        config (CrawlerConfig): Configuration for the crawler. Override it to set custom configuration.

    """

    logger: logging.Logger
    config: CrawlerConfig = CrawlerConfig()

    _queue: asyncio.Queue

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._queue = asyncio.Queue()

    @abstractmethod
    async def generate_requests(self) -> AsyncIterator[Request]:
        """Yields requests to be handled."""
        if False:  # pylint: disable=W0125
            yield Request(url="https://example.com", callback=lambda _: None)  # just a stub for mypy

    async def run(self) -> None:
        """Runs the crawler."""
        self.logger.info("Running crawler with config:\n%s", self.config.model_dump_json(indent=2))

        async for request in self.generate_requests():
            await self._queue.put(request)

        workers = [asyncio.create_task(self._worker()) for _ in range(self.config.workers)]
        await self._queue.join()
        for worker in workers:
            worker.cancel()

    async def _worker(self) -> None:
        """Worker to handle requests from the queue."""
        while True:
            request = await self._queue.get()
            try:
                await self._handle_request(request)
            except Exception as exc:  # pylint: disable=W0718
                self.logger.error("Error handling request %s: %s", request, exc)
            finally:
                self._queue.task_done()

    async def _handle_request(self, request: Request) -> None:
        """Handles the `request`."""
        self.logger.info("Handling request: %s", request)

        async with AsyncClient() as client:
            request_kwargs: dict[str, Any] = {
                "method": request.method,
                "url": request.url,
                "params": request.query_params,
                "headers": request.headers,
                "cookies": request.cookies,
                "data": request.form_data,
                "json": request.json_data,
                "files": request.files,
            }
            if request.auth is not None:
                request_kwargs["auth"] = request.auth
            if request.timeout is not None:
                request_kwargs["timeout"] = Timeout(request.timeout.total_seconds())
            if request.follow_redirects is not None:
                request_kwargs["follow_redirects"] = request.follow_redirects
            httpx_response = await client.request(**request_kwargs)

        response = Response.from_httpx_response(httpx_response, request)
        self.logger.debug("Got response: %s", response)

        callback_result = request.callback(response)
        if hasattr(callback_result, "__aiter__"):
            async for item in callback_result:
                if isinstance(item, Request):
                    await self._queue.put(item)
        else:
            await callback_result