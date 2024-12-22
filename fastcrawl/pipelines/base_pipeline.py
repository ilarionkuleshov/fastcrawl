from abc import ABC, abstractmethod
from typing import Any


class BasePipeline(ABC):
    """Base for all pipelines."""

    @abstractmethod
    async def process_item(self, item: Any) -> Any | None:
        """Processes an item returned by the crawler.

        Args:
            item (Any): Item to process.

        Returns:
            Any: Processed item.
            None: If the item should be dropped and not passed to the next pipelines.

        """

    async def on_crawler_start(self) -> None:
        """Called when the crawler starts."""

    async def on_crawler_finish(self) -> None:
        """Called when the crawler finishes."""
