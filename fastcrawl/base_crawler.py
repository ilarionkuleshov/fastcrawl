import asyncio
import logging
from abc import ABC, abstractmethod
from typing import AsyncIterator, Optional

from httpx import AsyncClient, Limits

from fastcrawl.models import CrawlerSettings, CrawlerStats, Request, Response


class BaseCrawler(ABC):
    """Base for all crawlers.

    Args:
        settings (Optional[CrawlerSettings]): Settings for the crawler.
            If not provided, the default settings will be used. Default is None.

    Attributes:
        logger (logging.Logger): Logger for the crawler.
        settings (CrawlerSettings): Settings for the crawler. Override it to set custom settings.
        stats (CrawlerStats): Statistics for the crawler.

    """

    logger: logging.Logger
    settings: CrawlerSettings = CrawlerSettings()
    stats: CrawlerStats

    _queue: asyncio.Queue
    _http_client: AsyncClient

    def __init__(self, settings: Optional[CrawlerSettings] = None) -> None:
        if settings:
            self.settings = settings

        if self.settings.setup_logging:
            self._setup_logging()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.stats = CrawlerStats()
        self._queue = asyncio.Queue()
        self._http_client = AsyncClient(**self._get_http_client_kwargs())

    def _setup_logging(self) -> None:
        """Sets up logging for the crawler."""
        logging.basicConfig(
            level=self.settings.logging.level,
            format=self.settings.logging.format,
        )
        logging.getLogger("asyncio").setLevel(self.settings.logging.level_asyncio)
        logging.getLogger("httpx").setLevel(self.settings.logging.level_httpx)
        logging.getLogger("httpcore").setLevel(self.settings.logging.level_httpcore)

    def _get_http_client_kwargs(self):
        kwargs = self.settings.http_client.model_dump()
        kwargs["params"] = kwargs.pop("query_params")
        kwargs["trust_env"] = False
        kwargs["limits"] = Limits(
            max_connections=kwargs.pop("max_connections"),
            max_keepalive_connections=kwargs.pop("max_keepalive_connections"),
            keepalive_expiry=kwargs.pop("keepalive_expiry"),
        )
        return kwargs

    @abstractmethod
    async def generate_requests(self) -> AsyncIterator[Request]:
        """Yields requests to be processed."""
        if False:  # pylint: disable=W0125  # pragma: no cover
            yield Request(url="https://example.com/", callback=lambda _: None)  # just a stub for mypy

    async def run(self) -> None:
        """Runs the crawler."""
        self.logger.info("Running crawler with settings: %s", self.settings.model_dump_json(indent=2))
        self.stats.start_crawling()
        for pipeline in self.settings.pipelines:
            await pipeline.on_crawler_start()

        async for request in self.generate_requests():
            await self._queue.put(request)

        workers = [asyncio.create_task(self._worker()) for _ in range(self.settings.workers)]
        await self._queue.join()
        for worker in workers:
            worker.cancel()

        await self._http_client.aclose()

        for pipeline in self.settings.pipelines:
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
                self.logger.error("Error processing request %s: %s", request, exc)
            finally:
                self._queue.task_done()

    async def _process_request(self, request: Request) -> None:
        """Executes the request, callback and processes the results.

        Args:
            request (Request): The request to process.

        """
        self.logger.debug("Processing request: %s", request)
        self.stats.add_request()

        request_kwargs = request.model_dump(exclude_none=True, exclude={"callback"})
        if "query_params" in request_kwargs:
            request_kwargs["params"] = request_kwargs.pop("query_params")
        if "form_data" in request_kwargs:
            request_kwargs["data"] = request_kwargs.pop("form_data")
        if "json_data" in request_kwargs:
            request_kwargs["json"] = request_kwargs.pop("json_data")
        httpx_response = await self._http_client.request(**request_kwargs)

        response = await Response.from_httpx_response(httpx_response, request)
        self.logger.debug("Got response: %s", response)
        self.stats.add_response(response.status_code)

        callback_result = request.callback(response)
        if hasattr(callback_result, "__aiter__"):
            async for item in callback_result:
                if isinstance(item, Request):
                    await self._queue.put(item)
                elif item is not None:
                    for pipeline in self.settings.pipelines:
                        item = await pipeline.process_item_with_check(item)
                        if item is None:
                            break
                    else:
                        self.stats.add_item()
        else:
            await callback_result
