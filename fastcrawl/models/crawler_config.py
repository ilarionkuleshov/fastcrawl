from typing import Annotated

from pydantic import BaseModel, ConfigDict
from pydantic.functional_serializers import PlainSerializer

from fastcrawl.base_pipeline import BasePipeline


class CrawlerLoggingConfig(BaseModel):
    """Crawler logging configuration model.

    Attributes:
        level (str): Logging level for the crawler. Default is "INFO".
        format (str): Logging format for the crawler.
            Default is "%(asctime)s [%(name)s] %(levelname)s: %(message)s".
        level_asyncio (str): Logging level for asyncio library. Default is "WARNING".
        level_httpx (str): Logging level for httpx library. Default is "WARNING".
        level_httpcore (str): Logging level for httpcore library. Default is "WARNING".

    """

    level: str = "INFO"
    format: str = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
    level_asyncio: str = "WARNING"
    level_httpx: str = "WARNING"
    level_httpcore: str = "WARNING"


class CrawlerConfig(BaseModel):
    """Crawler configuration model.

    Attributes:
        workers (int): Number of workers to process requests. Default is 15.
        pipelines (list[BasePipeline]): List of pipelines to process responses.
            Pipelines will be executed in the order they are defined. Default is [].
        configure_logging (bool): Whether to configure logging for the crawler. Default is True.
        logging (CrawlerLoggingConfig): Logging configuration for the crawler. Default is CrawlerLoggingConfig().

    """

    workers: int = 15
    pipelines: list[Annotated[BasePipeline, PlainSerializer(str)]] = []
    configure_logging: bool = True
    logging: CrawlerLoggingConfig = CrawlerLoggingConfig()

    model_config = ConfigDict(arbitrary_types_allowed=True)
