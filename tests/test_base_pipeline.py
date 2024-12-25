import pytest

from fastcrawl import BasePipeline


class MockPipeline(BasePipeline[str]):
    """A mock class for testing the `BasePipeline` class."""

    async def process_item(self, item: str) -> str | None:
        """See `BasePipeline` class."""
        return item * 2


def test_logger() -> None:
    """Tests the `logger` attribute of the `BasePipeline` class."""
    pipeline = MockPipeline()
    assert pipeline.logger.name == "MockPipeline"


def test_expected_type() -> None:
    """Tests the `_expected_type` attribute of the `BasePipeline` class."""
    pipeline = MockPipeline()
    assert pipeline._expected_type is str  # pylint: disable=W0212


@pytest.mark.asyncio
async def test_process_item_with_check() -> None:
    """Tests the `process_item_with_check` method of the `BasePipeline` class."""
    pipeline = MockPipeline()
    assert await pipeline.process_item_with_check("test") == await pipeline.process_item("test")
    assert await pipeline.process_item_with_check(1) == 1


def test_str() -> None:
    """Tests the `__str__` method of the `BasePipeline` class."""
    pipeline = MockPipeline()
    assert str(pipeline) == "<MockPipeline[str]>"
