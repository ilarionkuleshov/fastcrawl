import asyncio
import logging
from abc import ABC, abstractmethod
from typing import AsyncIterator

from httpx import AsyncClient, Timeout

from fastcrawl.models import CrawlerConfig, CrawlerStats, Request, Response


class BaseCrawler(ABC):
    """Base for all crawlers.

    Attributes:
        logger (logging.Logger): Logger for the crawler.
        config (CrawlerConfig): Configuration for the crawler. Override it to set custom configuration.
        stats (CrawlerStats): Statistics for the crawler.

    """

    logger: logging.Logger
    config: CrawlerConfig = CrawlerConfig()
    stats: CrawlerStats

    _queue: asyncio.Queue

    def __init__(self) -> None:
        if self.config.configure_logging:
            self._configure_logging()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.stats = CrawlerStats()
        self._queue = asyncio.Queue()

    def _configure_logging(self) -> None:
        """Configures logging for the crawler."""
        logging.basicConfig(
            level=self.config.log_level,
            format=self.config.log_format,
        )
        logging.getLogger("asyncio").setLevel(self.config.log_level_asyncio)
        logging.getLogger("httpx").setLevel(self.config.log_level_httpx)
        logging.getLogger("httpcore").setLevel(self.config.log_level_httpcore)

    @abstractmethod
    async def generate_requests(self) -> AsyncIterator[Request]:
        """Yields requests to be processed."""
        if False:  # pylint: disable=W0125
            yield Request(url="https://example.com", callback=lambda _: None)  # just a stub for mypy

    async def run(self) -> None:
        """Runs the crawler."""
        self.logger.info("Running crawler with config: %s", self.config.model_dump_json(indent=2))
        self.stats.start_crawling()
        for pipeline in self.config.pipelines:
            await pipeline.on_crawler_start()

        async for request in self.generate_requests():
            await self._queue.put(request)

        workers = [asyncio.create_task(self._worker()) for _ in range(self.config.workers)]
        await self._queue.join()
        for worker in workers:
            worker.cancel()

        for pipeline in self.config.pipelines:
            await pipeline.on_crawler_finish()
        self.stats.finish_crawling()
        self.logger.info("Crawling finished with stats: %s", self.stats.model_dump_json(indent=2))

    async def _worker(self) -> None:
        """Worker to process requests from the queue."""
        while True:
            request = await self._queue.get()
            try:
                await self._process_request(request)
            except Exception as exc:  # pylint: disable=W0718
                self.logger.error("Error handling request %s: %s", request, exc)
            finally:
                self._queue.task_done()

    async def _process_request(self, request: Request) -> None:
        """Processes the `request`."""
        self.logger.debug("Handling request: %s", request)
        self.stats.add_request()

        async with AsyncClient() as client:
            request_kwargs = request.model_dump(by_alias=True, exclude_none=True, exclude={"callback"})
            if "timeout" in request_kwargs:
                request_kwargs["timeout"] = Timeout(request_kwargs["timeout"].total_seconds())
            httpx_response = await client.request(**request_kwargs)

        response = Response.from_httpx_response(httpx_response, request)
        self.logger.debug("Got response: %s", response)
        self.stats.add_response(response.status_code)

        callback_result = request.callback(response)
        if hasattr(callback_result, "__aiter__"):
            async for item in callback_result:
                if isinstance(item, Request):
                    await self._queue.put(item)
                elif item is not None:
                    for pipeline in self.config.pipelines:
                        item = await pipeline.process_item_with_check(item)
                        if item is None:
                            break
                    else:
                        self.stats.add_item()
        else:
            await callback_result
