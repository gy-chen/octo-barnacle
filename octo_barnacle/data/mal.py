"""Functions for obtaining data from MyAnimeList

RecommendationPager
    obtain page content from https://myanimelist.net/recommendations.php?s=recentrecs&t=anime

RecommendationParser
    parse content of https://myanimelist.net/recommendations.php?s=recentrecs&t=anime page
"""
import itertools
import enum
import time
import requests
from bs4 import BeautifulSoup


class RecommendationType(enum.Enum):
    ANIME = 'anime'
    MANGA = 'manga'


class RecommendationPager:

    BASE_URL = 'https://myanimelist.net/recommendations.php?s=recentrecs'

    def __init__(self, downloader, type_=None):
        """init

        Args:
            downloader (octo_barnacle.data.downloader.Downloader): for downloading content
            type_ (RecommendationType): type of recommendation want to download
        """
        self._downloader = downloader
        self._type = type_
        if self._type is None:
            self._type = RecommendationType.ANIME

    def get(self, page):
        """Get content of specific page

        Args:
            page (int): page number, start from 0

        Raises:
            PageNotFoundError: raise if page is not exists (usually is reached end of pages)

        Return:
            page content
        """
        show_param = self._convert_to_show_param(page)
        url = "{}&show={}&t={}".format(
            self.BASE_URL, self._convert_to_show_param(page), self._type.value)
        try:
            return self._downloader.download(url)
        except requests.HTTPError as e:
            if e.response.status_code != 404:
                raise
            raise PageNotFoundError()

    def _convert_to_show_param(self, page):
        """show param 100 equal to page 1, 200 equal to page 2, ...etc"""
        return int(page) * 100

    def __iter__(self):
        try:
            for page in itertools.count():
                yield self.get(page)
        except PageNotFoundError:
            return


class CharacterPager:
    """CharacterPager

    get MyAnimeList characters page content

    Args:
        downloader (octo_barnacle.data.downloader.Downloader): for downloading content
    """

    BASE_URL = 'https://myanimelist.net/character.php'

    def __init__(self, downloader):
        self._downloader = downloader

    def get(self, page):
        """Get content of specific page

        Args:
            page (int): page number, start from 0

        Raises:
            PageNotFoundError: raise if page is not exists (usually is reached end of pages)

        Return:
            page content
        """
        url = '{}?limit={:d}'.format(
            self.BASE_URL, self._convert_to_limit_param(page))
        content = self._downloader.download(url)
        if self._is_page_empty(content):
            raise PageNotFoundError()
        return content

    def _convert_to_limit_param(self, page):
        "seems a page contains 50 items, so limit = page * 50"
        return int(page * 50)

    def _is_page_empty(self, content):
        return not BeautifulSoup(content).find_all(class_="ranking-list")

    def __iter__(self):
        try:
            for page in itertools.count():
                yield self.get(page)
        except PageNotFoundError:
            return


class PageNotFoundError(Exception):
    pass


class RecommendationParser:

    def parse(self, content):
        """Parse recommendation page content

        Args:
            content (str): page content of recommendation page

        Return:
            list of dict that contain recommendations
        """
        soup = BeautifulSoup(content, 'html.parser')
        content = soup.find(id='content')
        recomm_raws = content.find_all(class_='borderClass')
        return [self._parse_recomm(recomm_raw) for recomm_raw in recomm_raws]

    def _parse_recomm(self, recomm_raw):
        return {
            'from': self._parse_from(recomm_raw),
            'to': self._parse_to(recomm_raw),
            'description': self._parse_description(recomm_raw)
        }

    def _parse_from(self, recomm_raw):
        content = recomm_raw.find_all('td')[0]
        return self._parse_anime(content)

    def _parse_to(self, recomm_raw):
        content = recomm_raw.find_all('td')[1]
        return self._parse_anime(content)

    def _parse_anime(self, anime):
        img_link = anime.find('img')['data-src']
        title = anime.find('strong').string
        return {
            'img_link': img_link,
            'title': title
        }

    def _parse_description(self, recomm_raw):
        return recomm_raw.find(class_='recommendations-user-recs-text').string


class CharacterParser:
    """CharacterParser

    parse MyAnimeList character page content.
    """

    def parse(self, content):
        """parse content of MAL character page content

        Args:
            content (str): MAL character page content, usually get from CharacterPager

        Return:
            list of dict in format: 
                {
                    'people': {
                        'name': 'character name',
                        'img_link': 'character image link'
                    },
                    'rank': rank number,
                    'animeography': [
                        'anime name',
                        ...
                    ],
                    'mangaography': [
                        'manga name',
                        ...
                    ],
                    'favorites': favorites number
                }
        """
        return [self._parse_ranking(ranking_content) for ranking_content in self._parse_ranking_list(content)]

    def _parse_ranking_list(self, content):
        return BeautifulSoup(content).find_all(class_="ranking-list")

    def _parse_ranking(self, ranking_soup):
        rank_soup = ranking_soup.find(class_='rank')
        people_soup = ranking_soup.find(class_='people')
        animeography_soup = ranking_soup.find(class_='animeography')
        mangaography_soup = ranking_soup.find(class_='mangaography')
        favorites_soup = ranking_soup.find(class_='favorites')
        return {
            'rank': self._to_int(rank_soup.get_text()),
            'people': self._parse_people(people_soup),
            'animeography': self._parse_animeography(animeography_soup),
            'mangaography': self._parse_mangaography(mangaography_soup),
            'favorites': self._to_int(favorites_soup.get_text())
        }

    def _parse_people(self, people_soup):
        name = people_soup.get_text(strip=True)
        img_link = people_soup.find('img')['data-src']
        return {
            'name': name,
            'img_link': img_link
        }

    def _parse_animeography(self, animeography_soup):
        return [title_soup.get_text(strip=True) for title_soup in animeography_soup.find_all(class_='title')]

    def _parse_mangaography(self, mangaography_soup):
        return [title_soup.get_text(strip=True) for title_soup in mangaography_soup.find_all(class_='title')]

    def _to_int(self, text):
        return int(''.join(d for d in text if d.isdigit()))
