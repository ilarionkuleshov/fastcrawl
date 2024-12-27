import logging
from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar, get_args

T = TypeVar("T")


class BasePipeline(ABC, Generic[T]):
    """Base for all pipelines.

    Attributes:
        logger (logging.Logger): Logger for the crawler.

    """

    logger: logging.Logger
    _expected_type: type[T]

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._expected_type = get_args(self.__orig_bases__[0])[0]  # type: ignore[attr-defined]  # pylint: disable=E1101

    async def process_item_with_check(self, item: Any) -> Any:
        """Processes an item with type checking.

        Note:
            If the item is not an instance of the expected type, it will be returned as is.

        Args:
            item (Any): Item to process.

        Returns:
            Any: Processed item or the item itself.

        """
        if not isinstance(item, self._expected_type):
            return item
        return await self.process_item(item)

    @abstractmethod
    async def process_item(self, item: T) -> Optional[T]:
        """Processes an item returned by the crawler.

        Args:
            item (T): Item to process.

        Returns:
            T: Processed item.
            None: If the item should be dropped and not passed to the next pipelines.

        """

    async def on_crawler_start(self) -> None:
        """Called when the crawler starts."""

    async def on_crawler_finish(self) -> None:
        """Called when the crawler finishes."""

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}[{self._expected_type.__name__}]>"
