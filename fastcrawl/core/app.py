import asyncio
import logging
from typing import Any, Optional

from fastcrawl import models
from fastcrawl.core.crawl_base import CrawlBase


class FastCrawl(CrawlBase):
    _task_queue: asyncio.Queue

    def __init__(self, name: str = "FastCrawl", settings: Optional[models.AppSettings] = None) -> None:
        settings = settings or models.AppSettings()
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
            await self._task_queue.put(await self._fetch_request(task))
        elif isinstance(task, models.Response):
            for new_task in self._process_response(task):
                await self._task_queue.put(new_task)
        else:
            self._process_item(task)
