import pytest

from fastcrawl import FastCrawl, Response


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
