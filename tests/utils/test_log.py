from logging import FileHandler
from pathlib import Path

from fastcrawl import LogSettings
from fastcrawl.utils.log import get_logger


def test_get_logger(tmp_path: Path) -> None:
    """Tests the `get_logger` function.

    Args:
        tmp_path (Path): A temporary path for the log file.

    """
    logger = get_logger("test", LogSettings(file=tmp_path / "test.log"))

    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], FileHandler)
    assert logger.handlers[0].formatter is not None
