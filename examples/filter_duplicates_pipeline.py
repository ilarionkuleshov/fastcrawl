import asyncio
from typing import AsyncIterator

from pydantic import BaseModel

from fastcrawl import BaseCrawler, BasePipeline, CrawlerConfig, Request, Response


class ExampleItem(BaseModel):
    """Example item model."""

    id: str
    title: str


class FilterDuplicatesPipeline(BasePipeline[ExampleItem]):
    """Pipeline that filters out duplicate items based on their IDs."""

    unique_ids: set[str]

    def __init__(self):
        super().__init__()
        self.unique_ids = set()

    async def process_item(self, item: ExampleItem) -> ExampleItem | None:
        """See `Pipeline` class."""
        if item.id in self.unique_ids:
            self.logger.info("Duplicate item: %s", item)
            return None
        self.unique_ids.add(item.id)
        return item


class ExampleCrawler(BaseCrawler):
    """Crawler that uses the `FilterDuplicatesPipeline`."""

    config = CrawlerConfig(pipelines=[FilterDuplicatesPipeline()])

    async def generate_requests(self) -> AsyncIterator[Request]:
        """See `Crawler` class."""
        for _ in range(3):
            yield Request(url="https://httpbin.org/html", callback=self.parse)

    async def parse(self, response: Response) -> AsyncIterator[ExampleItem]:
        """Yields example items with IDs and titles."""
        title = response.selector.xpath(".//h1/text()").get() or "unknown"
        yield ExampleItem(id=str(response.url), title=title)


if __name__ == "__main__":
    asyncio.run(ExampleCrawler().run())
