import json
from typing import Any

from httpx import URL
from pydantic import BaseModel, ConfigDict

from fastcrawl.models.request import Request


class Response(BaseModel):
    """Response model.

    Attributes:
        url (URL): URL of the response.
        status_code (int): Status code of the response.
        content (bytes | None): Content of the response. Default is None.
        text (str | None): Text of the response. Default is None.
        headers (dict[str, str] | None): Headers of the response. Default is None.
        cookies (dict[str, str] | None): Cookies of the response. Default is None.
        request (Request): Request that generated the response.

    """

    url: URL
    status_code: int
    content: bytes | None = None
    text: str | None = None
    headers: dict[str, str] | None = None
    cookies: dict[str, str] | None = None
    request: Request

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def get_json(self) -> Any | None:
        """Returns JSON representation of the response."""
        return json.loads(self.text) if self.text is not None else None
