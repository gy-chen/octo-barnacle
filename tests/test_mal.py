from octo_barnacle.data import mal


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
