"""Functions for obtaining data from MyAnimeList

RecommendationPager
    obtain page content from https://myanimelist.net/recommendations.php?s=recentrecs&t=anime

RecommendationParser
    parse content of https://myanimelist.net/recommendations.php?s=recentrecs&t=anime page
"""
import itertools
import requests


class RecommendationPager:

    BASE_URL = 'https://myanimelist.net/recommendations.php?s=recentrecs&t=anime'

    def get(self, page):
        """Get content of specific page

        Args:
            page (int): page number, start from 0

        Raises:
            NotFoundError: raise if page is not exists (usually is reached end of pages)

        Return:
            page content
        """
        show_param = self._convert_to_show_param(page)
        url = "{}&show={}".format(
            self.BASE_URL, self._convert_to_show_param(page))
        res = requests.get(url)
        res.raise_for_status()
        return res.text

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


class RecommendationParser:

    def parse(self, content):
        """Parse recommendation page content 

        Args:
            content (str): page content of recommendation page

        Return:
            list of dict that contain recommendations
        """
        # TODO
        pass
