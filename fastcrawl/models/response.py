import json
from typing import Any, Optional

import httpx
import parsel
from pydantic import BaseModel, ConfigDict, PrivateAttr

from fastcrawl.models.request import Request


class Response(BaseModel):
    url: httpx.URL
    status_code: int
    is_success: bool
    content: bytes
    text: str
    headers: Optional[dict[str, str]] = None
    cookies: Optional[dict[str, str]] = None
    request: Request
    _cached_selector: Optional[parsel.Selector] = PrivateAttr(default=None)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    async def from_httpx_response(cls, httpx_response: httpx.Response, request: Request) -> "Response":
        try:
            content = httpx_response.content
        except httpx.ResponseNotRead:
            content = await httpx_response.aread()

        return cls(
            url=httpx_response.url,
            status_code=httpx_response.status_code,
            is_success=httpx_response.is_success,
            content=content,
            text=httpx_response.text,
            headers=dict(httpx_response.headers),
            cookies=dict(httpx_response.cookies),
            request=request,
        )

    def get_json_data(self) -> Any:
        return json.loads(self.text)

    @property
    def selector(self) -> parsel.Selector:
        if self._cached_selector is None:
            self._cached_selector = parsel.Selector(text=self.text)
        return self._cached_selector

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}({self.status_code}, {self.url})>"
