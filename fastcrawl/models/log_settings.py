import pathlib
from typing import Optional, Union

from pydantic import BaseModel


class LogSettings(BaseModel):
    configure_globally: bool = True
    level: str = "INFO"
    logger_name_suffix: Optional[str] = None
    format: str = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
    file: Optional[Union[pathlib.Path, str]] = None
    level_asyncio: str = "WARNING"
    level_httpx: str = "WARNING"
    level_httpcore: str = "WARNING"
