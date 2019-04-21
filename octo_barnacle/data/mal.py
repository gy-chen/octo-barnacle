"""Functions for obtaining data from MyAnimeList

RecommendationPager
    obtain page content from https://myanimelist.net/recommendations.php?s=recentrecs&t=anime

RecommendationParser
    parse content of https://myanimelist.net/recommendations.php?s=recentrecs&t=anime page
"""


class RecommendationPager:

    def get(self, page):
        """Get content of specific page

        Args:
            page (int): page number, start from 0

        Raises:
            NotFoundError: raise if page is not exists (usually is reached end of pages)

        Return:
            page content
        """
        # TODO
        pass

    def __iter__(self):
        # TODO
        pass


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
