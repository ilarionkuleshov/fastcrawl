from datetime import datetime

from freezegun import freeze_time

from fastcrawl.models import CrawlerStats


def test_start_crawling_and_finish_crawling() -> None:
    """Tests the `start_crawling` and `finish_crawling` methods of the `CrawlerStats` class."""
    stats = CrawlerStats()
    frozen_datetime = datetime(1, 1, 1)

    with freeze_time(frozen_datetime):
        stats.start_crawling()
        stats.finish_crawling()

    assert stats.started_at == frozen_datetime
    assert stats.finished_at == frozen_datetime


def test_add_request() -> None:
    """Tests the `add_request` method of the `CrawlerStats` class."""
    stats = CrawlerStats()
    stats.add_request()
    assert stats.requests == 1
    stats.add_request()
    assert stats.requests == 2


def test_add_response() -> None:
    """Tests the `add_response` method of the `CrawlerStats` class."""
    stats = CrawlerStats()
    stats.add_response(200)
    assert stats.responses_by_codes == {200: 1}
    stats.add_response(200)
    assert stats.responses_by_codes == {200: 2}
    stats.add_response(404)
    assert stats.responses_by_codes == {200: 2, 404: 1}


def test_add_item() -> None:
    """Tests the `add_item` method of the `CrawlerStats` class."""
    stats = CrawlerStats()
    stats.add_item()
    assert stats.items == 1
    stats.add_item()
    assert stats.items == 2
