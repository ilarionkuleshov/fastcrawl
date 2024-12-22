from typing import Annotated

from pydantic import BaseModel, ConfigDict
from pydantic.functional_serializers import PlainSerializer

from fastcrawl.pipelines import BasePipeline


class CrawlerConfig(BaseModel):
    """Crawler configuration model.

    Attributes:
        workers (int): Number of workers to process requests. Default is 15.
        pipelines (list[BasePipeline]): List of pipelines to process responses.
            Pipelines will be executed in the order they are defined. Default is [].
        configure_logging (bool): Whether to configure logging for the crawler. Default is True.
        log_level (str): Logging level for the crawler. Default is "INFO".
        log_level_asyncio (str): Logging level for asyncio library. Default is "WARNING".
        log_level_httpx (str): Logging level for httpx library. Default is "WARNING".
        log_level_httpcore (str): Logging level for httpcore library. Default is "WARNING".
        log_format (str): Logging format for the crawler.
            Default is "%(asctime)s [%(name)s] %(levelname)s: %(message)s".

    """

    workers: int = 15
    pipelines: list[Annotated[BasePipeline, PlainSerializer(str)]] = []
    configure_logging: bool = True
    log_level: str = "INFO"
    log_level_asyncio: str = "WARNING"
    log_level_httpx: str = "WARNING"
    log_level_httpcore: str = "WARNING"
    log_format: str = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"

    model_config = ConfigDict(arbitrary_types_allowed=True)
