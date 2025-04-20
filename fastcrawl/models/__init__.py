from .crawler_settings import CrawlerSettings
from .crawler_stats import CrawlerStats
from .http_client_settings import HttpClientSettings
from .log_settings import LogSettings
from .request import Request
from .response import Response

# required for pydantic 2.11+
Response.model_rebuild()
Request.model_rebuild()
