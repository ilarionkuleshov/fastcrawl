import asyncio
import logging
from typing import Any, Optional

from fastcrawl import models
from fastcrawl.core.crawl_base import CrawlBase


class FastCrawl(CrawlBase):
    """FastCrawl application.

    Args:
        name (str): Name of the application. Defaults to "FastCrawl".
        settings (Optional[models.Settings]): Application settings.
            If not provided, default settings are used. Defaults to None.

    """

    _task_queue: asyncio.Queue

    def __init__(self, name: str = "FastCrawl", settings: Optional[models.Settings] = None) -> None:
        settings = settings or models.Settings()
        self._setup_logging(settings.log)

        super().__init__(name=name, settings=settings)
        self._task_queue = asyncio.Queue()

    def _setup_logging(self, settings: models.LogSettings) -> None:
        if settings.configure_globally:
            logging.basicConfig(level=settings.level, format=settings.format)

        logging.getLogger("asyncio").setLevel(settings.level_asyncio)
        logging.getLogger("httpx").setLevel(settings.level_httpx)
        logging.getLogger("httpcore").setLevel(settings.level_httpcore)

    async def run(self) -> None:
        """Runs the FastCrawl application."""
        for task in self._start_tasks:
            await self._task_queue.put(task)

        workers = [asyncio.create_task(self._worker()) for _ in range(self.settings.workers)]
        await self._task_queue.join()
        for worker in workers:
            worker.cancel()

        await self._http_client.aclose()

    async def _worker(self) -> None:
        while True:
            task = await self._task_queue.get()
            try:
                await self._process_task(task)
            except Exception:
                self.logger.exception("Error processing task: %s", task)
            self._task_queue.task_done()

    async def _process_task(self, task: Any) -> None:
        if isinstance(task, models.Request):
            await self._task_queue.put(await self._process_request(task))
        elif isinstance(task, models.Response):
            for new_task in self._process_response(task):
                await self._task_queue.put(new_task)
        else:
            self._process_item(task)
