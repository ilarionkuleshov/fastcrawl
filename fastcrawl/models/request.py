from httpx import URL
from pydantic import BaseModel, ConfigDict, Field

from fastcrawl.types import (
    Auth,
    Cookies,
    Files,
    FormData,
    Headers,
    JsonData,
    QueryParams,
    RequestCallback,
)


class Request(BaseModel):
    """Request model.

    Attributes:
        method (str): HTTP method. Default is "GET".
        url (URL | str): URL to request.
        callback (RequestCallback): Callback to process the response.
        query_params (QueryParams | None): Query parameters for the URL. Default is None.
        headers (Headers | None): Headers for the request. Default is None.
        cookies (Cookies | None): Cookies for the request. Default is None.
        form_data (FormData | None): Form data for the request. Default is None.
        json_data (JsonData | None): JSON data for the request. Default is None.
        files (Files | None): Files for the request. Default is None.
        auth (Auth | None): Authentication credentials. Default is None.
        timeout (float | None): Timeout for the request in seconds. Default is None.
        follow_redirects (bool | None): Whether to follow redirects. Default is None.

    """

    method: str = "GET"
    url: URL | str
    callback: RequestCallback
    query_params: QueryParams | None = Field(default=None, alias="params")
    headers: Headers | None = None
    cookies: Cookies | None = None
    form_data: FormData | None = Field(default=None, alias="data")
    json_data: JsonData | None = Field(default=None, alias="json")
    files: Files | None = None
    auth: Auth | None = None
    timeout: float | None = None
    follow_redirects: bool | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}({self.method}, {self.url})>"
