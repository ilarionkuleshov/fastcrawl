from pydantic import BaseModel


class CrawlerConfig(BaseModel):
    """Crawler configuration model.

    Attributes:
        workers (int): Number of workers to handle requests. Default is 15.

    """

    workers: int = 15
