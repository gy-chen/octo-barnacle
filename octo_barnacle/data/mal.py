"""Functions for obtaining data from MyAnimeList

RecommendationPager
    obtain page content from https://myanimelist.net/recommendations.php?s=recentrecs&t=anime

RecommendationParser
    parse content of https://myanimelist.net/recommendations.php?s=recentrecs&t=anime page
"""
import itertools
import time
import requests
from bs4 import BeautifulSoup


class RecommendationPager:

    USER_AGENT = 'OctoBarnacle/0.1 (+https://github.com/gy-chen/octo-barnacle)'
    BASE_URL = 'https://myanimelist.net/recommendations.php?s=recentrecs&t=anime'

    def __init__(self, delay=None):
        """init

        Args:
            delay (int): delay in seconds between every requests
        """
        self._delay = delay
        self._last_req_time = None

    def get(self, page):
        """Get content of specific page

        Args:
            page (int): page number, start from 0

        Raises:
            NotFoundError: raise if page is not exists (usually is reached end of pages)

        Return:
            page content
        """
        try:
            self._ensure_delay()
        except _DelayError:
            time.sleep(self._delay)
            return self.get(page)
        show_param = self._convert_to_show_param(page)
        url = "{}&show={}".format(
            self.BASE_URL, self._convert_to_show_param(page))

        headers = {}
        if self.USER_AGENT:
            headers['user-agent'] = self.USER_AGENT
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        return res.text

    def _ensure_delay(self):
        if self._delay is None:
            return
        if self._last_req_time is None:
            self._last_req_time = time.time()
            return
        if self._delay > time.time() - self._last_req_time:
            raise _DelayError()

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
