from typing import Annotated

from httpx import URL
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_serializers import PlainSerializer

from fastcrawl.base_pipeline import BasePipeline
from fastcrawl.types import Auth, Cookies, Headers, QueryParams


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


class CrawlerHttpClientConfig(BaseModel):
    """Crawler HTTP client configuration model.

    Attributes:
        base_url (URL | str): Base URL for the HTTP client. Default is "".
        auth (Auth | None): Authentication for the HTTP client. Default is None.
        query_params (QueryParams | None): Query parameters for the HTTP client. Default is None.
        headers (Headers | None): Headers for the HTTP client. Default is None.
        cookies (Cookies | None): Cookies for the HTTP client. Default is None.
        verify (bool): Whether to verify SSL certificates. Default is True.
        http1 (bool): Whether to use HTTP/1.1. Default is True.
        http2 (bool): Whether to use HTTP/2. Default is False.
        proxy (URL | str | None): Proxy for the HTTP client. Default is None.
        timeout (float): Timeout for the HTTP client. Default is 5.0.
        max_connections (int | None): Specifies the maximum number of concurrent connections allowed. Default is 100.
        max_keepalive_connections (int | None): The maximum number of keep-alive connections the pool can maintain.
            Must not exceed `max_connections`. Default is 20.
        keepalive_expiry (float | None): The maximum duration in seconds that a keep-alive
            connection can remain idle. Default is 5.0.
        follow_redirects (bool): Whether to follow redirects. Default is False.
        max_redirects (int): Maximum number of redirects to follow. Default is 20.
        default_encoding (str): Default encoding for the HTTP client. Default is "utf-8".

    """

    base_url: URL | str = ""
    auth: Auth | None = None
    query_params: QueryParams | None = Field(default=None, alias="params")
    headers: Headers | None = None
    cookies: Cookies | None = None
    verify: bool = True
    http1: bool = True
    http2: bool = False
    proxy: URL | str | None = None
    timeout: float = 5.0
    max_connections: int | None = 100
    max_keepalive_connections: int | None = 20
    keepalive_expiry: float | None = 5.0
    follow_redirects: bool = False
    max_redirects: int = 20
    default_encoding: str = "utf-8"

    model_config = ConfigDict(arbitrary_types_allowed=True)


class CrawlerConfig(BaseModel):
    """Crawler configuration model.

    Attributes:
        workers (int): Number of workers to process requests. Default is 15.
        pipelines (list[BasePipeline]): List of pipelines to process responses.
            Pipelines will be executed in the order they are defined. Default is [].
        configure_logging (bool): Whether to configure logging for the crawler. Default is True.
        logging (CrawlerLoggingConfig): Logging configuration for the crawler. Default is CrawlerLoggingConfig().
        http_client (CrawlerHttpClientConfig): HTTP client configuration for the crawler.
            Default is CrawlerHttpClientConfig().

    """

    workers: int = 15
    pipelines: list[Annotated[BasePipeline, PlainSerializer(str)]] = []
    configure_logging: bool = True
    logging: CrawlerLoggingConfig = CrawlerLoggingConfig()
    http_client: CrawlerHttpClientConfig = CrawlerHttpClientConfig()

    model_config = ConfigDict(arbitrary_types_allowed=True)
