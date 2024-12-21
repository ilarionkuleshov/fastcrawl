import json
from typing import Any

from httpx import URL
from httpx import Response as HttpxResponse
from httpx import ResponseNotRead
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
        request (Request): Request used to fetch the response.

    """

    url: URL
    status_code: int
    content: bytes | None = None
    text: str | None = None
    headers: dict[str, str] | None = None
    cookies: dict[str, str] | None = None
    request: Request

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def from_httpx_response(cls, httpx_response: HttpxResponse, request: Request) -> "Response":
        """Returns new instance from an httpx response.

        Args:
            httpx_response (HttpxResponse): Response from httpx.
            request (Request): Request used to fetch the response.

        """
        try:
            content = httpx_response.content
            text = httpx_response.text
        except ResponseNotRead:
            content = None
            text = None
        return cls(
            url=httpx_response.url,
            status_code=httpx_response.status_code,
            content=content,
            text=text,
            headers=dict(httpx_response.headers),
            cookies=dict(httpx_response.cookies),
            request=request,
        )

    def get_json(self) -> Any | None:
        """Returns JSON representation of the response."""
        return json.loads(self.text) if self.text is not None else None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.status_code}, {self.url})>"
