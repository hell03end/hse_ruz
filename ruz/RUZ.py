import json
from http.client import HTTPResponse
from urllib import error, parse, request

from .utils import RUZ_API_ENDPOINTS, RUZ_API_URL, Logger


class RUZ(object):
    ''' Handler for RUZ API '''

    def __init__(self, strict_v1: bool=False, **kwargs):
        '''
            >>> RUZ(base_url=None)
            Traceback (most recent call last):
                ...
            PermissionError: Can't get base url!
        '''
        self._url = kwargs.pop('base_url', RUZ_API_URL)
        if not self._url:
            raise PermissionError("Can't get base url!")
        self._endpoints = kwargs.pop('endpoints', RUZ_API_ENDPOINTS)
        self._url2 = self._url
        self._logger = Logger(str(self.__class__))
        if not strict_v1:
            self._url2 += r"v2/"
        super(RUZ, self).__init__()

    @property
    def v(self) -> int:
        ''' Max API version '''
        return 2 if self._url2[-2] == "2" else 1

    def _make_url(self, endpoint: str, data: dict=None, v: int=1) -> str:
        ''' Creates full url for API requests '''
        url = self._url if v == 1 else self._url2
        if data:
            return "{}{}?{}".format(url, self._endpoints[endpoint],
                                    parse.urlencode(data).encode('utf-8'))
        return "{}{}".format(url, self._endpoints[endpoint])

    def _request(self, endpoint: str, data: dict=None) -> HTTPResponse:
        ''' Implements request to API with given params '''
        try:
            return request.urlopen(self._make_url(endpoint, data, v=2))
        except error.HTTPError as excinfo:
            self._logger.warning("v2 API unavailable: %s", excinfo)
        return request.urlopen(self._make_url(endpoint, data))

    def get(self, endpoint: str, **params) -> dict:
        ''' Return requested data in JSON '''
        try:
            response = self._request(endpoint, data=params)
            return json.loads(response.read().decode('utf-8'))
        except error.HTTPError as excinfo:
            self._logger.error(excinfo)
            return {}


if __name__ == "__main__":
    import doctest
    doctest.testmod()
