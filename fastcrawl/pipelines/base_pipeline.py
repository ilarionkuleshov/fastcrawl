from abc import ABC, abstractmethod

from pydantic import BaseModel


class BasePipeline(ABC):
    """Base for all pipelines."""

    @abstractmethod
    async def process_item(self, item: BaseModel) -> BaseModel | None:
        """Processes an item returned by the crawler.

        Args:
            item (BaseModel): Item to process.

        Returns:
            BaseModel: Processed item.
            None: If the item should be dropped and not passed to the next pipelines.

        """

    async def on_crawler_start(self) -> None:
        """Called when the crawler starts."""

    async def on_crawler_finish(self) -> None:
        """Called when the crawler finishes."""
