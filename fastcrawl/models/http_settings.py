from typing import Optional, Union

import httpx
from pydantic import BaseModel, ConfigDict

from fastcrawl import types_


class HttpSettings(BaseModel):

    base_url: Union[httpx.URL, str] = ""
    auth: Optional[types_.Auth] = None
    query_params: Optional[types_.QueryParams] = None
    headers: Optional[types_.Headers] = None
    cookies: Optional[types_.Cookies] = None
    verify: bool = True
    http1: bool = True
    http2: bool = False
    proxy: Optional[Union[httpx.URL, str]] = None
    timeout: float = 5.0
    max_connections: Optional[int] = 100
    max_keepalive_connections: Optional[int] = 20
    keepalive_expiry: Optional[float] = 5.0
    follow_redirects: bool = False
    max_redirects: int = 20
    default_encoding: str = "utf-8"

    model_config = ConfigDict(arbitrary_types_allowed=True)
