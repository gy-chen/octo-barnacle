import pytest
import os
from octo_barnacle.data import mal

base_path = os.path.dirname(__file__)


@pytest.fixture
def sample_mal_page0():
    sample_path = os.path.join(base_path, 'sample_mal_page0.html')
    with open(sample_path, 'r') as f:
        return f.read()


def test_pager():
    pager = mal.RecommendationPager()

    page0 = pager.get(0)
    assert '<title>Anime Recommendations - MyAnimeList.net\n</title>' in page0
    assert '[1]' in page0

    page1 = pager.get(1)
    assert '<title>Anime Recommendations - MyAnimeList.net\n</title>' in page1
    assert '[2]' in page1


def test_pager_iter():
    pager = mal.RecommendationPager()

    pager_iter = iter(pager)
    page0 = next(pager_iter)
    assert '<title>Anime Recommendations - MyAnimeList.net\n</title>' in page0
    assert '[1]' in page0

    page1 = next(pager_iter)
    assert '<title>Anime Recommendations - MyAnimeList.net\n</title>' in page1
    assert '[2]' in page1


def test_parser(sample_mal_page0):
    parser = mal.RecommendationParser()

    result = parser.parse(sample_mal_page0)
    assert len(result) == 100

    assert result[2]['from']['title'] == 'Sen to Chihiro no Kamikakushi'
    assert result[2]['from']['img_link'] == 'https://cdn.myanimelist.net/images/anime/6/79597t.jpg'
    assert result[2]['to']['title'] == 'Irozuku Sekai no Ashita kara'
    assert result[2]['to']['img_link'] == 'https://cdn.myanimelist.net/images/anime/1424/93855t.jpg'
    assert result[2]['description'] == '- Creative supernatural and magical concepts (including some which reminded me specifically of this particular film).\n- Similar concept of girl attempting to fit into a world different from their own\n- Beautiful artistry on par with many Miyazaki films\n'


def test_run():
    pager = mal.RecommendationPager()
    parser = mal.RecommendationParser()

    for page in range(5):
        page_content = pager.get(page)
        assert len(parser.parse(page_content)) == 100
