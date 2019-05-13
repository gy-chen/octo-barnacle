import time
import pytest
import requests
from octo_barnacle.data import downloader


@pytest.fixture
def url():
    return 'https://myanimelist.net/recommendations.php?s=recentrecs&t=anime'


@pytest.fixture
def url_404():
    return 'http://example.org/404'


def test_downloader(url):
    downloader_ = downloader.Downloader()
    content = downloader_.download(url)
    assert isinstance(content, str)


def test_error(url_404):
    downloader_ = downloader.Downloader()
    with pytest.raises(requests.HTTPError):
        downloader_.download(url_404)


def test_delay(url):
    start_time = time.time()
    downloader_ = downloader.Downloader(delay=10)
    for _ in range(2):
        downloader_.download(url)
    assert time.time() - start_time > 10
