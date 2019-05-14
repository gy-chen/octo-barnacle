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
        except requests.HTTPError as e:
            if e.response.status_code != 404:
                raise e


class PageNotFoundError(Exception):
    pass


class _DelayError(Exception):
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
