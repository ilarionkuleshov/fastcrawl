import asyncio
import logging
from abc import ABC, abstractmethod
from asyncio import Task
from typing import Any, AsyncIterator

from httpx import AsyncClient, Timeout

from fastcrawl.models import Request, Response


class Crawler(ABC):
    """Base for all crawlers.

    Attributes:
        logger (logging.Logger): Logger for the crawler.

    """

    logger: logging.Logger
    _request_tasks: list[Task]

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._request_tasks = []

    @abstractmethod
    async def generate_requests(self) -> AsyncIterator[Request]:
        """Yields requests to be processed."""
        if False:  # pylint: disable=W0125
            yield Request(url="https://example.com", callback=lambda _: None)  # just a stub for mypy

    async def run(self) -> None:
        """Runs the crawler."""
        async for request in self.generate_requests():
            self._create_request_task(request)
        await asyncio.gather(*self._request_tasks)

    def _create_request_task(self, request: Request) -> None:
        """Creates a task to handle the `request`."""
        task = asyncio.create_task(self._handle_request(request))
        self._request_tasks.append(task)

    async def _handle_request(self, request: Request) -> None:
        """Handles the `request`."""
        self.logger.debug("Request: %s", request)

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
                request_kwargs["allow_redirects"] = request.follow_redirects
            httpx_response = await client.request(**request_kwargs)

        response = Response.from_httpx_response(httpx_response, request)
        self.logger.debug("Response: %s", response)

        callback_result = request.callback(response)
        if hasattr(callback_result, "__aiter__"):
            async for item in callback_result:
                if isinstance(item, Request):
                    self._create_request_task(item)
        else:
            await callback_result
