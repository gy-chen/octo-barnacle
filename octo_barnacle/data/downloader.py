"""Provide features for downloading data from web

Downloader
    class that can specific delay between each download requests
"""
import time
import requests
from requests.adapters import HTTPAdapter


class Downloader:

    USER_AGENT = 'OctoBarnacle/0.1 (+https://github.com/gy-chen/octo-barnacle)'

    def __init__(self, delay=None):
        """init

        Args:
            delay (int): delay between each requests in seconds.
        """
        self._session = requests.Session()
        # TODO add this in config
        self._session.mount('http://', HTTPAdapter(max_retries=3))
        self._delay = delay
        self._last_req_time = None

    def download(self, url):
        """download content of specific url

        Args:
            url (str)

        Raises:
            requests.HTTPError: if encouter error while downloading

        Return:
            str content
        """
        try:
            self._ensure_delay()
        except _DelayError:
            time.sleep(self._delay)
            return self.download(url)

        headers = {}
        if self.USER_AGENT:
            headers['user-agent'] = self.USER_AGENT
        res = self._session.get(url, headers=headers)
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


class _DelayError(Exception):
    pass
