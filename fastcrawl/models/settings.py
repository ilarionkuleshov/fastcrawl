from pydantic_settings import BaseSettings, SettingsConfigDict

from fastcrawl.models.http_settings import HttpSettings
from fastcrawl.models.log_settings import LogSettings


class Settings(BaseSettings):
    """Settings for FastCrawl application or crawler.

    Settings can be retrieved from environment variables.
    Environment variables should be prefixed with `FASTCRAWL_` and nested attributes
    should be separated by double underscores (e.g., `FASTCRAWL_WORKERS` or `FASTCRAWL_LOG__LEVEL`).

    Attributes:
        workers (int): Number of worker threads to use for crawling. Defaults to 15.
        log (LogSettings): Logging settings. Defaults to LogSettings().
        http (HttpSettings): HTTP settings for requests. Defaults to HttpSettings().

    """

    workers: int = 15
    log: LogSettings = LogSettings()
    http: HttpSettings = HttpSettings()

    model_config = SettingsConfigDict(
        env_prefix="fastcrawl_",
        env_nested_delimiter="__",
        extra="ignore",
    )
