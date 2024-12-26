from typing import Annotated, Optional, Union

from dotenv import find_dotenv
from httpx import URL
from pydantic import BaseModel, ConfigDict
from pydantic.functional_serializers import PlainSerializer
from pydantic_settings import BaseSettings, SettingsConfigDict

from fastcrawl.base_pipeline import BasePipeline
from fastcrawl.types import Auth, Cookies, Headers, QueryParams


class CrawlerLoggingSettings(BaseModel):
    """Crawler logging settings model.

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


class CrawlerHttpClientSettings(BaseModel):
    """Crawler HTTP client settings model.

    Attributes:
        base_url (Union[URL, str]): Base URL for the HTTP client. Default is "".
        auth (Optional[Auth]): Authentication for the HTTP client. Default is None.
        query_params (Optional[QueryParams]): Query parameters for the HTTP client. Default is None.
        headers (Optional[Headers]): Headers for the HTTP client. Default is None.
        cookies (Optional[Cookies]): Cookies for the HTTP client. Default is None.
        verify (bool): Whether to verify SSL certificates. Default is True.
        http1 (bool): Whether to use HTTP/1.1. Default is True.
        http2 (bool): Whether to use HTTP/2. Default is False.
        proxy (Optional[Union[URL, str]]): Proxy for the HTTP client. Default is None.
        timeout (float): Timeout for the HTTP client. Default is 5.0.
        max_connections (Optional[int]): Specifies the maximum number of concurrent connections allowed. Default is 100.
        max_keepalive_connections (Optional[int]): The maximum number of keep-alive connections the pool can maintain.
            Must not exceed `max_connections`. Default is 20.
        keepalive_expiry (Optional[float]): The maximum duration in seconds that a keep-alive
            connection can remain idle. Default is 5.0.
        follow_redirects (bool): Whether to follow redirects. Default is False.
        max_redirects (int): Maximum number of redirects to follow. Default is 20.
        default_encoding (str): Default encoding for the HTTP client. Default is "utf-8".

    """

    base_url: Union[URL, str] = ""
    auth: Optional[Auth] = None
    query_params: Optional[QueryParams] = None
    headers: Optional[Headers] = None
    cookies: Optional[Cookies] = None
    verify: bool = True
    http1: bool = True
    http2: bool = False
    proxy: Optional[Union[URL, str]] = None
    timeout: float = 5.0
    max_connections: Optional[int] = 100
    max_keepalive_connections: Optional[int] = 20
    keepalive_expiry: Optional[float] = 5.0
    follow_redirects: bool = False
    max_redirects: int = 20
    default_encoding: str = "utf-8"

    model_config = ConfigDict(arbitrary_types_allowed=True)


class CrawlerSettings(BaseSettings):
    """Crawler settings model.

    Attributes:
        workers (int): Number of workers to process requests. Default is 15.
        pipelines (list[BasePipeline]): List of pipelines to process responses.
            Pipelines will be executed in the order they are defined. Default is [].
        setup_logging (bool): Whether to setup logging for the crawler. Default is True.
        logging (CrawlerLoggingSettings): Logging settings for the crawler. Default is CrawlerLoggingSettings().
        http_client (CrawlerHttpClientSettings): HTTP client settings for the crawler.
            Default is CrawlerHttpClientSettings().

    """

    workers: int = 15
    pipelines: list[Annotated[BasePipeline, PlainSerializer(str)]] = []
    setup_logging: bool = True
    logging: CrawlerLoggingSettings = CrawlerLoggingSettings()
    http_client: CrawlerHttpClientSettings = CrawlerHttpClientSettings()

    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
        env_prefix="fastcrawl_",
        env_nested_delimiter="__",
        extra="ignore",
    )
