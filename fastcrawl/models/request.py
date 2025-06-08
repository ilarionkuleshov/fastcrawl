from typing import Callable, Optional, Union

import httpx
from pydantic import BaseModel, ConfigDict

from fastcrawl import types_


class Request(BaseModel):
    method: str = "GET"
    url: Union[httpx.URL, str]
    handler: Callable
    query_params: Optional[types_.QueryParams] = None
    headers: Optional[types_.Headers] = None
    cookies: Optional[types_.Cookies] = None
    form_data: Optional[types_.FormData] = None
    json_data: Optional[types_.JsonData] = None
    files: Optional[types_.Files] = None
    auth: Optional[types_.Auth] = None
    timeout: Optional[float] = None
    follow_redirects: Optional[bool] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}({self.method}, {self.url})>"
