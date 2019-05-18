import os
import bson
import pytest
import requests
from octo_barnacle.data import mal
from octo_barnacle.data.downloader import Downloader

base_path = os.path.dirname(__file__)


@pytest.fixture
def sample_mal_page0():
    sample_path = os.path.join(base_path, 'sample_mal_page0.html')
    with open(sample_path, 'r') as f:
        return f.read()


@pytest.fixture
def sample_manga_mal_page0():
    sample_path = os.path.join(base_path, 'sample_manga_mal_page0.html')
    with open(sample_path, 'r') as f:
        return f.read()


@pytest.fixture
def sample_mal_character_page_empty():
    sample_path = os.path.join(
        base_path, 'sample_mal_character_page_empty.html')
    with open(sample_path, 'r') as f:
        return f.read()


@pytest.fixture
def sample_mal_character_page_0():
    sample_path = os.path.join(
        base_path, 'sample_mal_character_page_0.html')
    with open(sample_path, 'r') as f:
        return f.read()


@pytest.fixture
def sample_mal_character_page_0_ranking_list():
    sample_path = os.path.join(
        base_path, 'sample_mal_character_page_0.bson')
    with open(sample_path, 'rb') as f:
        return bson.BSON.decode(f.read())['ranking_list']


@pytest.fixture
def downloader():
    return Downloader(3)


def test_pager(downloader):
    pager = mal.RecommendationPager(downloader)

    page0 = pager.get(0)
    assert '<title>Anime Recommendations - MyAnimeList.net\n</title>' in page0
    assert '[1]' in page0

    page1 = pager.get(1)
    assert '<title>Anime Recommendations - MyAnimeList.net\n</title>' in page1
    assert '[2]' in page1


def test_manga_pager(downloader):
    pager = mal.RecommendationPager(downloader, mal.RecommendationType.MANGA)

    page0 = pager.get(0)
    assert '<title>Manga Recommendations - MyAnimeList.net\n</title>' in page0
    assert '[1]' in page0

    page1 = pager.get(1)
    assert '<title>Manga Recommendations - MyAnimeList.net\n</title>' in page1
    assert '[2]' in page1


def test_pager_iter(downloader):
    pager = mal.RecommendationPager(downloader)

    pager_iter = iter(pager)
    page0 = next(pager_iter)
    assert '<title>Anime Recommendations - MyAnimeList.net\n</title>' in page0
    assert '[1]' in page0

    page1 = next(pager_iter)
    assert '<title>Anime Recommendations - MyAnimeList.net\n</title>' in page1
    assert '[2]' in page1


def test_manga_pager_iter(downloader):
    pager = mal.RecommendationPager(downloader, mal.RecommendationType.MANGA)

    pager_iter = iter(pager)
    page0 = next(pager_iter)
    assert '<title>Manga Recommendations - MyAnimeList.net\n</title>' in page0
    assert '[1]' in page0

    page1 = next(pager_iter)
    assert '<title>Manga Recommendations - MyAnimeList.net\n</title>' in page1
    assert '[2]' in page1


def test_pager_not_found(downloader):
    pager = mal.RecommendationPager(downloader)
    with pytest.raises(mal.PageNotFoundError):
        pager.get(1e9)


def test_parser(sample_mal_page0):
    parser = mal.RecommendationParser()

    result = parser.parse(sample_mal_page0)
    assert len(result) == 100

    assert result[2]['from']['title'] == 'Sen to Chihiro no Kamikakushi'
    assert result[2]['from']['img_link'] == 'https://cdn.myanimelist.net/images/anime/6/79597t.jpg'
    assert result[2]['to']['title'] == 'Irozuku Sekai no Ashita kara'
    assert result[2]['to']['img_link'] == 'https://cdn.myanimelist.net/images/anime/1424/93855t.jpg'
    assert result[2]['description'] == '- Creative supernatural and magical concepts (including some which reminded me specifically of this particular film).\n- Similar concept of girl attempting to fit into a world different from their own\n- Beautiful artistry on par with many Miyazaki films\n'


def test_manga_parser(sample_manga_mal_page0):
    parser = mal.RecommendationParser()

    result = parser.parse(sample_manga_mal_page0)
    assert len(result) == 100

    assert result[2]['from']['title'] == 'Ueki no Housoku'
    assert result[2]['from']['img_link'] == 'https://cdn.myanimelist.net/images/manga/3/160943t.jpg'
    assert result[2]['to']['title'] == 'Deatte 5-byou de Battle'
    assert result[2]['to']['img_link'] == 'https://cdn.myanimelist.net/images/manga/2/185911t.jpg'
    assert result[2]['description'] == 'they actually really similar to each other \n-Ueki is a light/happy manga and Deatte 5-byou is just a little bit darker of Ueki.\nsimilarities:\n-the characters gained unique abilities.\n-they both have battle/tournament.\n-MC gain team/trust of others.\n'


def test_run(downloader):
    pager = mal.RecommendationPager(downloader)
    parser = mal.RecommendationParser()

    for page in range(5):
        page_content = pager.get(page)
        assert len(parser.parse(page_content)) == 100


def test_character_pager(downloader):
    pager = mal.CharacterPager(downloader)

    with pytest.raises(mal.PageNotFoundError):
        pager.get(1e9)


def test_character_parser(sample_mal_character_page_0, sample_mal_character_page_0_ranking_list):
    parser = mal.CharacterParser()

    ranking_list = parser.parse(sample_mal_character_page_0)

    assert len(ranking_list) == 50
    assert ranking_list == sample_mal_character_page_0_ranking_list


def test_character_parser_empty(sample_mal_character_page_empty):
    parser = mal.CharacterParser()

    ranking_list = parser.parse(sample_mal_character_page_empty)
    assert len(ranking_list) == 0
