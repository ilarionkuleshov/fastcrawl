from typing import Annotated, Type

from dotenv import find_dotenv
from pydantic.functional_serializers import PlainSerializer
from pydantic_settings import BaseSettings, SettingsConfigDict

from fastcrawl.base_pipeline import BasePipeline
from fastcrawl.models.http_client_settings import HttpClientSettings
from fastcrawl.models.log_settings import LogSettings


class CrawlerSettings(BaseSettings):
    """Crawler settings model.

    Attributes:
        workers (int): Number of workers to process requests. Default is 15.
        pipelines (list[Type[BasePipeline]]): List of pipelines to process items.
            Pipelines will be executed in the order they are defined. Default is [].
        log (LogSettings): Log settings for the crawler. Default is LogSettings().
        http_client (HttpClientSettings): HTTP client settings for the crawler. Default is HttpClientSettings().

    """

    workers: int = 15
    pipelines: list[Annotated[Type[BasePipeline], PlainSerializer(lambda x: x.__name__)]] = []
    log: LogSettings = LogSettings()
    http_client: HttpClientSettings = HttpClientSettings()

    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
        env_prefix="fastcrawl_",
        env_nested_delimiter="__",
        extra="ignore",
    )
