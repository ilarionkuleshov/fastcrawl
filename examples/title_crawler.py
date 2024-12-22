import asyncio
from typing import AsyncIterator

from fastcrawl import Crawler, Request, Response


class TitleCrawler(Crawler):
    """Simple crawler for extracting the title of an HTML page."""

    async def generate_requests(self) -> AsyncIterator[Request]:
        """See `Crawler` class."""
        yield Request(url="https://httpbin.org/html", callback=self.parse)

    async def parse(self, response: Response) -> None:
        """Extracts and logs the title of the HTML page."""
        title = response.selector.xpath(".//h1/text()").get()
        self.logger.info("Title of the page %s: %s", response.url, title)


if __name__ == "__main__":
    asyncio.run(TitleCrawler().run())
