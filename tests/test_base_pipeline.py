import pytest

from tests.mocks import MockStrPipeline


def test_logger() -> None:
    """Tests the `logger` attribute of the `BasePipeline` class."""
    pipeline = MockStrPipeline()
    assert pipeline.logger.name == "MockStrPipeline"


@pytest.mark.asyncio
async def test_process_allowed_item() -> None:
    """Tests the `process_allowed_item` method of the `BasePipeline` class."""
    pipeline = MockStrPipeline()
    assert await pipeline.process_allowed_item(
        "test"
    ) == await pipeline.process_item("test")
    assert await pipeline.process_allowed_item(1) == 1
