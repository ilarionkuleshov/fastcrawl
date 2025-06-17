from typing import Iterator

import pytest
from pydantic import BaseModel
from pytest_httpx import HTTPXMock
from pytest_mock import MockerFixture

from fastcrawl import FastCrawl, Request, Response


def test_handler_without_annotations():
    app = FastCrawl()

    with pytest.raises(TypeError):

        @app.handler()
        def my_handler(response):
            pass


def test_handler_without_response_arg():
    app = FastCrawl()

    with pytest.raises(TypeError):

        @app.handler()
        def my_handler():
            pass


def test_handler_with_invalid_response_arg():
    app = FastCrawl()

    with pytest.raises(TypeError):

        @app.handler()
        def my_handler(response: str):
            pass


def test_handler_with_invalid_return_type():
    app = FastCrawl()

    with pytest.raises(TypeError):

        @app.handler()
        def my_handler(response: Response) -> str:
            pass


def test_handler_with_invalid_url():
    app = FastCrawl()

    with pytest.raises(TypeError):

        @app.handler(123)
        def my_handler(response: Response):
            pass


def test_handler_with_few_urls():
    app = FastCrawl()

    @app.handler("http://example1.com", "http://example2.com")
    def my_handler(response: Response):
        pass

    assert len(app._start_tasks) == 2


@pytest.mark.asyncio
async def test_handler_called(httpx_mock: HTTPXMock, mocker: MockerFixture):
    app = FastCrawl()

    handler_mock = mocker.Mock()

    @app.handler("http://example.com")
    def my_handler(response: Response):
        handler_mock()

    httpx_mock.add_response()
    await app.run()
    handler_mock.assert_called_once()


@pytest.mark.asyncio
async def test_handler_with_error(httpx_mock: HTTPXMock, caplog: pytest.LogCaptureFixture):
    app = FastCrawl()

    @app.handler("http://example.com")
    def my_handler(response: Response):
        raise ValueError

    httpx_mock.add_response()
    with caplog.at_level("INFO"):
        await app.run()

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "ERROR"


@pytest.mark.asyncio
async def test_few_handlers(httpx_mock: HTTPXMock, mocker: MockerFixture):
    app = FastCrawl()

    handler_mock = mocker.Mock()

    @app.handler("http://example.com")
    def my_handler_1(response: Response) -> Iterator[Request]:
        yield Request(url="http://example.com", handler=my_handler_2)

    @app.handler()
    def my_handler_2(response: Response):
        handler_mock()

    httpx_mock.add_response()
    httpx_mock.add_response()
    await app.run()
    handler_mock.assert_called_once()


@pytest.mark.asyncio
async def test_pipeline(httpx_mock: HTTPXMock, mocker: MockerFixture):
    app = FastCrawl()

    pipeline_mock = mocker.Mock()

    class MyItem(BaseModel):
        name: str

    expected_item_1 = MyItem(name="example1")
    expected_item_2 = MyItem(name="example2")
    expected_item_3 = MyItem(name="example3")

    @app.handler("http://example.com")
    def my_handler(response: Response) -> Iterator[MyItem]:
        yield expected_item_1
        yield expected_item_2
        yield expected_item_3

    @app.pipeline()
    def my_pipeline(item: MyItem):
        pipeline_mock(item)

    httpx_mock.add_response()
    await app.run()
    pipeline_mock.assert_any_call(expected_item_1)
    pipeline_mock.assert_any_call(expected_item_2)
    pipeline_mock.assert_any_call(expected_item_3)


@pytest.mark.asyncio
async def test_few_pipelines(httpx_mock: HTTPXMock, mocker: MockerFixture):
    app = FastCrawl()

    pipeline_mock = mocker.Mock()

    class MyItem(BaseModel):
        name: str

    initial_item = MyItem(name="example1")

    @app.handler("http://example.com")
    def my_handler(response: Response) -> Iterator[MyItem]:
        yield initial_item

    @app.pipeline()
    def my_pipeline1(item: MyItem) -> MyItem:
        item.name = item.name.upper()
        return item

    @app.pipeline()
    def my_pipeline2(item: MyItem):
        pipeline_mock(item)

    httpx_mock.add_response()
    await app.run()
    pipeline_mock.assert_called_once_with(MyItem(name=initial_item.name.upper()))


@pytest.mark.asyncio
async def test_few_pipelines_with_priority(httpx_mock: HTTPXMock, mocker: MockerFixture):
    app = FastCrawl()

    pipeline_mock = mocker.Mock()

    class MyItem(BaseModel):
        name: str

    expected_item = MyItem(name="example1")

    @app.handler("http://example.com")
    def my_handler(response: Response) -> Iterator[MyItem]:
        yield expected_item

    @app.pipeline()
    def my_pipeline1(item: MyItem) -> MyItem:
        item.name = item.name.upper()
        return item

    @app.pipeline(priority=0)
    def my_pipeline2(item: MyItem):
        pipeline_mock(item)

    httpx_mock.add_response()
    await app.run()
    pipeline_mock.assert_called_once_with(expected_item)


def test_pipeline_without_item_arg():
    app = FastCrawl()

    with pytest.raises(TypeError):

        @app.pipeline()
        def my_pipeline():
            pass


def test_pipeline_with_invalid_item_arg():
    app = FastCrawl()

    with pytest.raises(TypeError):

        @app.pipeline()
        def my_pipeline(item: str):
            pass


def test_pipeline_with_invalid_return_type():
    app = FastCrawl()

    with pytest.raises(TypeError):

        @app.pipeline()
        def my_pipeline(item: Response) -> str:
            pass


def test_pipeline_with_invalid_priority():
    app = FastCrawl()

    with pytest.raises(TypeError):

        @app.pipeline(priority="high")
        def my_pipeline(item: Response):
            pass


@pytest.mark.asyncio
async def test_handler_with_custom_request(httpx_mock: HTTPXMock):
    app = FastCrawl()

    @app.handler("http://example.com")
    def my_handler_1(response: Response) -> Iterator[Request]:
        yield Request(
            url="http://example.com",
            handler=my_handler_2,
            query_params={"next": "true"},
            form_data={"key": "value"},
            json_data={"key": "value"},
        )

    @app.handler()
    def my_handler_2(response: Response):
        pass

    httpx_mock.add_response()
    httpx_mock.add_response()
    await app.run()


@pytest.mark.asyncio
async def test_handler_with_invalid_return(httpx_mock: HTTPXMock, caplog: pytest.LogCaptureFixture):
    app = FastCrawl()

    @app.handler("http://example.com")
    def my_handler_1(response: Response) -> Iterator[Request]:
        return 1

    @app.handler("http://example.com")
    def my_handler_2(response: Response) -> Iterator[Request]:
        yield "invalid"

    httpx_mock.add_response()
    httpx_mock.add_response()
    with caplog.at_level("INFO"):
        await app.run()

    assert len(caplog.records) == 2
    assert caplog.records[0].levelname == "ERROR"


@pytest.mark.asyncio
async def test_pipeline_with_invalid_return(httpx_mock: HTTPXMock, caplog: pytest.LogCaptureFixture):
    app = FastCrawl()

    class MyItem(BaseModel):
        name: str

    @app.handler("http://example.com")
    def my_handler(response: Response) -> Iterator[Request | MyItem]:
        yield MyItem(name="example1")

    @app.pipeline()
    def my_pipeline(item: MyItem) -> MyItem:
        pass

    httpx_mock.add_response()
    with caplog.at_level("INFO"):
        await app.run()

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "ERROR"


@pytest.mark.asyncio
async def test_pipeline_with_drop(httpx_mock: HTTPXMock, mocker: MockerFixture):
    app = FastCrawl()

    pipeline_mock = mocker.Mock()

    class MyItem(BaseModel):
        name: str

    @app.handler("http://example.com")
    def my_handler(response: Response) -> Iterator[MyItem]:
        yield MyItem(name="example1")

    @app.pipeline()
    def my_pipeline_1(item: MyItem) -> None:
        return None

    @app.pipeline()
    def my_pipeline_2(item: MyItem):
        pipeline_mock()

    httpx_mock.add_response()
    await app.run()
    pipeline_mock.assert_not_called()


@pytest.mark.asyncio
async def test_pipeline_with_invalid_item(httpx_mock: HTTPXMock, mocker: MockerFixture):
    app = FastCrawl()

    pipeline_mock = mocker.Mock()

    class MyItem1(BaseModel):
        name: str

    class MyItem2(BaseModel):
        name: str

    @app.handler("http://example.com")
    def my_handler(response: Response) -> Iterator[MyItem1]:
        yield MyItem1(name="example1")

    @app.pipeline()
    def my_pipeline(item: MyItem2):
        pipeline_mock()

    httpx_mock.add_response()
    await app.run()
    pipeline_mock.assert_not_called()
