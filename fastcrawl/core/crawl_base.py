import abc
import copy
import logging
from typing import Any, Callable, Iterator, Optional

import httpx
import pydantic

from fastcrawl import models
from fastcrawl.core import type_validation
from fastcrawl.core.component import Component


class CrawlBase(abc.ABC):

    name: str
    settings: models.AppSettings
    logger: logging.Logger

    _handlers: dict[Callable, Component]
    _pipelines: list[Component]
    _start_tasks: list[models.Request]
    _http_client: httpx.AsyncClient

    def __init__(self, name: str, settings: models.AppSettings) -> None:
        self.name = name
        self.settings = settings
        self.logger = logging.getLogger(name)

        self._handlers = {}
        self._pipelines = []
        self._start_tasks = []
        self._http_client = httpx.AsyncClient(**self._get_http_client_kwargs())

    def _get_http_client_kwargs(self) -> dict[str, Any]:
        kwargs = self.settings.http.model_dump()
        kwargs["params"] = kwargs.pop("query_params")
        kwargs["trust_env"] = False
        kwargs["limits"] = httpx.Limits(
            max_connections=kwargs.pop("max_connections"),
            max_keepalive_connections=kwargs.pop("max_keepalive_connections"),
            keepalive_expiry=kwargs.pop("keepalive_expiry"),
        )
        return kwargs

    def handler(self, *urls: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            validator = type_validation.TypeValidator(func)
            validator.validate_required_arg("response", models.Response)
            return_type = validator.validate_return_type(
                (pydantic.BaseModel, models.Request, type(None)), can_be_iterator=True
            )
            self._handlers[func] = Component(func, return_type)
            if urls:
                for url in urls:
                    if not isinstance(url, str):
                        raise TypeError(f"URL must be a string, got {type(url)}")
                    request = models.Request(url=url, handler=func)
                    self._start_tasks.append(request)
            return func

        return decorator

    def pipeline(self, priority: Optional[int] = None) -> Callable:
        def decorator(func: Callable) -> Callable:
            if priority is not None and priority < 0:
                raise ValueError("Priority must be a non-negative integer.")

            validator = type_validation.TypeValidator(func)
            item_type = validator.validate_required_arg("item", pydantic.BaseModel)
            return_type = validator.validate_return_type(expected_types=(item_type, type(None)), can_be_iterator=False)
            component = Component(func, return_type)
            if priority is None:
                self._pipelines.append(component)
            else:
                self._pipelines.insert(priority, component)

            return func

        return decorator

    async def _fetch_request(self, request: models.Request) -> models.Response:
        request_kwargs = request.model_dump(exclude_none=True, exclude={"handler"})
        if "query_params" in request_kwargs:
            request_kwargs["params"] = request_kwargs.pop("query_params")
        if "form_data" in request_kwargs:
            request_kwargs["data"] = request_kwargs.pop("form_data")
        if "json_data" in request_kwargs:
            request_kwargs["json"] = request_kwargs.pop("json_data")
        httpx_response = await self._http_client.request(**request_kwargs)
        response = await models.Response.from_httpx_response(httpx_response, request)
        self.logger.debug("Got response: %s", response)
        return response

    def _process_response(self, response: models.Response) -> Iterator[Any]:
        handler = self._handlers[response.request.handler]
        for result in handler.run_iter(response=response):
            yield result

    def _process_item(self, item: Any) -> None:
        processed_item = copy.deepcopy(item)
        for pipeline in self._pipelines:
            processed_item = pipeline.run(item=processed_item)
            if not item:
                break
