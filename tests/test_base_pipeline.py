import pytest

from tests.utils import MockStrPipeline


def test_logger() -> None:
    """Tests the `logger` attribute of the `BasePipeline` class."""
    pipeline = MockStrPipeline()
    assert pipeline.logger.name == "MockStrPipeline"


def test_expected_type() -> None:
    """Tests the `_expected_type` attribute of the `BasePipeline` class."""
    pipeline = MockStrPipeline()
    assert pipeline._expected_type is str  # pylint: disable=W0212


@pytest.mark.asyncio
async def test_process_item_with_check() -> None:
    """Tests the `process_item_with_check` method of the `BasePipeline` class."""
    pipeline = MockStrPipeline()
    assert await pipeline.process_item_with_check("test") == await pipeline.process_item("test")
    assert await pipeline.process_item_with_check(1) == 1
