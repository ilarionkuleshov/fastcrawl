import pathlib
from typing import Optional, Union

from pydantic import BaseModel


class LogSettings(BaseModel):
    """Logging settings.

    Attributes:
        configure_globally (bool): Whether to configure logging globally. Defaults to True.
        level (str): Logging level. Defaults to "INFO".
        format (str): Log message format. See model code for default value.
        file (Optional[Union[pathlib.Path, str]]): File path for logging output. Defaults to None.
        level_asyncio (str): Logging level for asyncio events. Defaults to "WARNING".
        level_httpx (str): Logging level for httpx requests. Defaults to "WARNING".
        level_httpcore (str): Logging level for httpcore requests. Defaults to "WARNING".

    """

    configure_globally: bool = True
    level: str = "INFO"
    format: str = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
    file: Optional[Union[pathlib.Path, str]] = None
    level_asyncio: str = "WARNING"
    level_httpx: str = "WARNING"
    level_httpcore: str = "WARNING"
